import { SudokuData } from "../types/index";

export const validateSudoku = (
    inputs: string[][],
    puzzleData: SudokuData | null
): { newConflicts: Set<string>; conflictingCells: Set<string> } => {
    if (!puzzleData) {
        return {
            newConflicts: new Set<string>(),
            conflictingCells: new Set<string>(),
        };
    }

    const newConflicts = new Set<string>();
    const conflictingCells = new Set<string>();

    // Check rows and columns
    for (let i = 0; i < 9; i++) {
        const rowSet = new Set<string>();
        const colSet = new Set<string>();
        for (let j = 0; j < 9; j++) {
            // Check row conflicts
            if (inputs[i][j] !== "." && rowSet.has(inputs[i][j])) {
                conflictingCells.add(`${i}-${j}`);
                for (let k = 0; k < 9; k++) {
                    newConflicts.add(`${i}-${k}`); // Add entire row to conflicts
                }
            } else {
                rowSet.add(inputs[i][j]);
            }

            // Check column conflicts
            if (inputs[j][i] !== "." && colSet.has(inputs[j][i])) {
                conflictingCells.add(`${j}-${i}`);
                for (let k = 0; k < 9; k++) {
                    newConflicts.add(`${k}-${i}`); // Add entire column to conflicts
                }
            } else {
                colSet.add(inputs[j][i]);
            }
        }
    }

    // Check 3x3 grids
    for (let blockRow = 0; blockRow < 3; blockRow++) {
        for (let blockCol = 0; blockCol < 3; blockCol++) {
            const squareSet = new Set<string>();
            for (let i = 0; i < 3; i++) {
                for (let j = 0; j < 3; j++) {
                    const rowIndex = blockRow * 3 + i;
                    const colIndex = blockCol * 3 + j;
                    if (
                        inputs[rowIndex][colIndex] !== "." &&
                        squareSet.has(inputs[rowIndex][colIndex])
                    ) {
                        conflictingCells.add(`${rowIndex}-${colIndex}`);
                        for (let k = 0; k < 3; k++) {
                            for (let l = 0; l < 3; l++) {
                                const r = blockRow * 3 + k;
                                const c = blockCol * 3 + l;
                                newConflicts.add(`${r}-${c}`); // Add entire block to conflicts
                            }
                        }
                    } else {
                        squareSet.add(inputs[rowIndex][colIndex]);
                    }
                }
            }
        }
    }

    return { newConflicts, conflictingCells };
};
