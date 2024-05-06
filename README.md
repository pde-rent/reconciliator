# Reconciliator

**Description:**

Reconciliator is a Python script designed to reconcile folders by identifying and handling various conflicts that may arise during synchronization or copying of files between directories. It provides features to identify duplicates across different directory trees, move missing files from source to destination, and identify versioned files that differ between source and destination.

**Example Usage:**

```bash
python reconciliator.py --dst /path/to/destination --src /path/to/source --rm-all-duplicates --simulate
```

- `--dst`: Specifies the destination folder where files are to be updated.
- `--src`: Specifies the source folder where files are to be removed.
- `--rm-all-duplicates`: (Optional) Removes all duplicate files found in the source folder.
- `--simulate`: (Optional) Simulates the operation without making any changes.

**Features:**

1. **Identifies Duplicates Across Different Trees:**
   - Reconciliator can detect duplicate files present in different directory trees, even if the filenames differ.
   - Duplicates are identified based on checksums to ensure accurate detection.

2. **Moves Missing Files From Source to Destination:**
   - Reconciliator automatically moves missing files from the source folder to the destination folder.
   - This ensures that both folders remain synchronized and up to date.

3. **Identifies Versioned Files With Differences:**
   - Version conflicts between files in the source and destination folders are detected.
   - Reconciliator identifies files with differing checksums and flags them as conflicts for manual resolution.

**Note:** Ensure that proper permissions are granted to perform file operations in both source and destination folders.

This script is useful for maintaining consistency and integrity when managing files across different directory structures.