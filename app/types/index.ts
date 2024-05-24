export interface SudokuData {
    id: number;
    puzzle: string[][];
    solution: string[][];
    clues: number;
    difficulty: string;
}