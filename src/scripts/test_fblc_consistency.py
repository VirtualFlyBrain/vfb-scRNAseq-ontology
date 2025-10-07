#!/usr/bin/env python3
"""
Test script to verify that no FBlc IDs have been lost between releases.
Compares FBlc IDs in current metadata_release_files with the previous release commit.
"""

import re
import subprocess
import sys
from pathlib import Path
import glob


def extract_fblc_ids_from_directory(directory_path):
    """
    Extract all unique FBlc IDs from OWL files in a directory.

    Args:
        directory_path: Path to directory containing OWL files

    Returns:
        Set of FBlc IDs found in the directory
    """
    all_ids = set()
    owl_files = list(Path(directory_path).glob('*.owl'))

    if not owl_files:
        print(f"WARNING: No OWL files found in {directory_path}")
        return all_ids

    print(f"Scanning {len(owl_files)} OWL files in {directory_path}...")

    for owl_file in owl_files:
        with open(owl_file, 'r') as f:
            content = f.read()
            ids = re.findall(r'FBlc\d{7}', content)
            all_ids.update(ids)

    return all_ids


def extract_fblc_ids_from_git_commit(commit_hash, directory_path):
    """
    Extract all FBlc IDs from metadata_release_files in a specific git commit.

    Args:
        commit_hash: Git commit hash or reference
        directory_path: Path to directory relative to repo root

    Returns:
        Set of FBlc IDs found in the commit
    """
    all_ids = set()

    # Get list of files from that commit
    result = subprocess.run(
        ['git', 'ls-tree', '-r', '--name-only', commit_hash, directory_path],
        capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        print(f"ERROR: Could not list files from commit {commit_hash}")
        print(result.stderr)
        sys.exit(1)

    files = [f for f in result.stdout.strip().split('\n') if f.endswith('.owl')]

    if not files:
        print(f"WARNING: No OWL files found in {directory_path} at commit {commit_hash}")
        return all_ids

    print(f"Scanning {len(files)} OWL files from commit {commit_hash}...")

    # Extract FBlc IDs from each file
    for file_path in files:
        result = subprocess.run(
            ['git', 'show', f'{commit_hash}:{file_path}'],
            capture_output=True, text=True, check=False
        )

        if result.returncode == 0:
            ids = re.findall(r'FBlc\d{7}', result.stdout)
            all_ids.update(ids)

    return all_ids


def get_previous_release_tag():
    """
    Get the most recent release tag (format: vYYYY-MM-DD).
    If HEAD is tagged with a release tag, gets the previous one.

    Returns:
        Tuple of (tag_name, commit_hash)
    """
    # Get all tags sorted by version (most recent first)
    result = subprocess.run(
        ['git', 'tag', '-l', 'v*', '--sort=-version:refname'],
        capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        print("ERROR: Could not list git tags")
        sys.exit(1)

    tags = [t.strip() for t in result.stdout.strip().split('\n') if t.strip()]

    if len(tags) < 1:
        print("ERROR: No release tags found (format: vYYYY-MM-DD)")
        sys.exit(1)

    # Check if HEAD is tagged with the most recent tag
    result = subprocess.run(
        ['git', 'describe', '--exact-match', '--tags', 'HEAD'],
        capture_output=True, text=True, check=False
    )

    current_tag = result.stdout.strip() if result.returncode == 0 else None

    # If HEAD is the most recent tag, use the second most recent; otherwise use most recent
    if current_tag and current_tag == tags[0] and len(tags) >= 2:
        previous_tag = tags[1]
    else:
        previous_tag = tags[0]

    # Get commit hash for the tag
    result = subprocess.run(
        ['git', 'rev-parse', previous_tag],
        capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        print(f"ERROR: Could not resolve tag {previous_tag}")
        sys.exit(1)

    commit_hash = result.stdout.strip()
    return previous_tag, commit_hash


def test_no_fblc_ids_lost(metadata_release_dir='metadata_release_files'):
    """
    Main test function to verify no FBlc IDs have been lost.

    Args:
        metadata_release_dir: Path to metadata_release_files directory

    Returns:
        0 if test passes, 1 if test fails
    """
    print("=" * 70)
    print("Testing FBlc ID consistency between releases")
    print("=" * 70)
    print()

    # Get previous release tag
    print("Finding previous release tag...")
    previous_tag, previous_commit = get_previous_release_tag()
    print(f"Previous release: {previous_tag} ({previous_commit[:7]})")
    print()

    # Extract IDs from previous release
    print("Extracting FBlc IDs from previous release...")
    previous_ids = extract_fblc_ids_from_git_commit(
        previous_commit,
        metadata_release_dir
    )
    print(f"Found {len(previous_ids)} unique FBlc IDs in previous release")
    print()

    # Extract IDs from current files
    print("Extracting FBlc IDs from current files...")
    current_ids = extract_fblc_ids_from_directory(metadata_release_dir)
    print(f"Found {len(current_ids)} unique FBlc IDs in current files")
    print()

    # Compare
    lost_ids = previous_ids - current_ids
    new_ids = current_ids - previous_ids

    # Report results
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Previous release ({previous_tag}): {len(previous_ids)} FBlc IDs")
    print(f"Current files:                  {len(current_ids)} FBlc IDs")
    print(f"New IDs added:                  {len(new_ids)}")
    print(f"IDs lost:                       {len(lost_ids)}")
    print()

    if new_ids:
        print(f"New FBlc IDs added ({len(new_ids)}):")
        for fblc_id in sorted(new_ids):
            print(f"  + {fblc_id}")
        print()

    if lost_ids:
        print(f"ERROR: Lost {len(lost_ids)} FBlc IDs:")
        for fblc_id in sorted(lost_ids):
            print(f"  - {fblc_id}")
        print()
        print("=" * 70)
        print("TEST FAILED: FBlc IDs have been lost!")
        print("=" * 70)
        return 1
    else:
        print("=" * 70)
        print("✓ TEST PASSED: No FBlc IDs lost")
        print("=" * 70)
        return 0


if __name__ == '__main__':
    # Find git repository root
    result = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        print("ERROR: Could not find git repository root")
        sys.exit(1)

    repo_root = Path(result.stdout.strip())
    metadata_dir = repo_root / 'metadata_release_files'

    # Run test
    exit_code = test_no_fblc_ids_lost(str(metadata_dir))
    sys.exit(exit_code)
