import { SudokuData } from "../types/index";

export const validateSudoku = (
    inputs: string[][],
    puzzleData: SudokuData | null
): { newConflicts: Set<string> } => {
    if (!puzzleData) {
        return { newConflicts: new Set<string>() };
    }

    const newConflicts = new Set<string>();

    const markDuplicates = (cells: Array<[number, number]>) => {
        const positions = new Map<string, string[]>();
        cells.forEach(([row, col]) => {
            const value = inputs[row][col];
            if (value !== ".") {
                positions.set(value, [
                    ...(positions.get(value) || []),
                    `${row}-${col}`,
                ]);
            }
        });
        positions.forEach((cellKeys) => {
            if (cellKeys.length > 1) {
                cellKeys.forEach((cellKey) => newConflicts.add(cellKey));
            }
        });
    };

    for (let index = 0; index < 9; index++) {
        markDuplicates(
            Array.from(
                { length: 9 },
                (_, col): [number, number] => [index, col]
            )
        );
        markDuplicates(
            Array.from(
                { length: 9 },
                (_, row): [number, number] => [row, index]
            )
        );
    }

    for (let blockRow = 0; blockRow < 3; blockRow++) {
        for (let blockCol = 0; blockCol < 3; blockCol++) {
            const cells: Array<[number, number]> = [];
            for (let row = 0; row < 3; row++) {
                for (let col = 0; col < 3; col++) {
                    cells.push([blockRow * 3 + row, blockCol * 3 + col]);
                }
            }
            markDuplicates(cells);
        }
    }

    return { newConflicts };
};
