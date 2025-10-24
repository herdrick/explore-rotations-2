# AGENTS.md

## Commands
- **Environment**: `conda activate amp-numpy-matplotlib-1`
- **After changes**: Run the modified script to find and fix problems  before committing
  - ** to run scripts**:
    - `python rotate_2d_live.py` - basic 2D rotation with sliders
    - `python conjugated_rotation_shape.py` - shape transformations via conjugation
    - `python conjugated_rotation_trajectory.py` - trajectory visualization of M = S⁻¹RS
  - **No tests** exist
  - if no errors commit the changes
    - Commit messages: append " :: Claude" to all commits

## Architecture
- Interactive matplotlib visualizations of rotation matrices
- All scripts use numpy for matrix operations and matplotlib sliders for real-time parameter adjustment

## Code Style
- Constants: uppercase (e.g., `P` for point matrix)
- Mathematical variables: single letters (e.g., `theta`, `R2`)
