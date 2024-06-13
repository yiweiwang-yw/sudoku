"use client";

import { useEffect, useState } from "react";
import {
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownItem,
    Button,
    user,
} from "@nextui-org/react";
import { SudokuData } from "./types/index";
import { validateSudoku } from "./components/validateSudoku";
import { defaultPuzzle } from "./components/defaultData";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export default function Home() {
    const [message, setMessage] = useState<string>("");
    const [puzzleData, setPuzzleData] = useState<SudokuData | null>(null);
    const [userInputs, setUserInputs] = useState<string[][]>([]);
    const [editedCells, setEditedCells] = useState<Set<string>>(new Set());
    const [conflicts, setConflicts] = useState<Set<string>>(new Set());
    const [initialCells, setInitialCells] = useState<Set<string>>(new Set());

    async function fetchRandomSudoku() {
        try {
            const response = await fetch(
                `${apiBaseUrl}/python/get_randomsudoku`
            );
            const data: SudokuData = await response.json();
            setMessage("Puzzle loaded");
            setPuzzleData(data);
            setUserInputs(data.puzzle.map((row) => row.slice()));

            // Track initial cells
            const initial = new Set<string>();
            data.puzzle.forEach((row, rowIndex) => {
                row.forEach((cell, colIndex) => {
                    if (cell !== ".") {
                        initial.add(`${rowIndex}-${colIndex}`);
                    }
                });
            });
            setInitialCells(initial);
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    async function fetchSudokuByDifficulty(difficulty: string) {
        try {
            const response = await fetch(`${apiBaseUrl}/python/sudoku/difficulty/${difficulty}`);
            const data: SudokuData = await response.json();
            setMessage(`Puzzle loaded with difficulty: ${difficulty}`);
            setPuzzleData(data);
            setUserInputs(data.puzzle.map((row: string[]) => row.slice()));
    
            // Track initial cells
            const initial = new Set<string>();
            data.puzzle.forEach((row: string[], rowIndex: number) => {
                row.forEach((cell: string, colIndex: number) => {
                    if (cell !== ".") {
                        initial.add(`${rowIndex}-${colIndex}`);
                    }
                });
            });
            setInitialCells(initial);
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    async function solveNextStep(puzzle: string[][]) {
        try {
            const response = await fetch(
                `${apiBaseUrl}/python/solve_next_step`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ puzzle }),
                }
            );
            console.log(JSON.stringify({ puzzle }));
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setMessage("Puzzle step solved");
            setPuzzleData(data);
            setUserInputs(data.puzzle.map((row: string[]) => row.slice()));

            // Track initial cells
            const initial = new Set<string>();
            data.puzzle.forEach((row: string[], rowIndex: number) => {
                row.forEach((cell: string, colIndex: number) => {
                    if (cell !== ".") {
                        initial.add(`${rowIndex}-${colIndex}`);
                    }
                });
            });
            setInitialCells(initial);
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to solve puzzle step");
        }
    }

    useEffect(() => {
        const initialPuzzleData = initializeEmptyBoard();
        setPuzzleData(initialPuzzleData);
        setUserInputs(initialPuzzleData.puzzle);
        setMessage("Puzzle loaded");
    }, []);

    const initializeEmptyBoard = () => {
        const randomDefaultPuzzle =
            defaultPuzzle[Math.floor(Math.random() * defaultPuzzle.length)];
        return {
            id: randomDefaultPuzzle.id,
            puzzle: randomDefaultPuzzle.puzzle,
            solution: randomDefaultPuzzle.solution,
            clues: randomDefaultPuzzle.clues,
            difficulty: randomDefaultPuzzle.difficulty,
        };
    };

    const clearSudokuBoard = () => {
        const emptyBoard = Array.from({ length: 9 }, () => Array(9).fill("."));
        setUserInputs(emptyBoard);
        setEditedCells(new Set());
        setInitialCells(new Set());
        setConflicts(new Set());
        setPuzzleData({
            id: 0,
            puzzle: emptyBoard,
            solution: emptyBoard,
            clues: 0,
            difficulty: "none",
        });
        setMessage("Board cleared");
    };

    const handleInputChange = (
        rowIndex: number,
        colIndex: number,
        value: string
    ) => {
        if (puzzleData) {
            const updatedInputs = userInputs.map((row, rIndex) =>
                row.map((cell, cIndex) => {
                    if (rIndex === rowIndex && cIndex === colIndex) {
                        return /^[1-9]$/.test(value) ? value : ".";
                    }
                    return cell;
                })
            );

            const updatedEditedCells = new Set(editedCells);
            updatedEditedCells.add(`${rowIndex}-${colIndex}`);

            setUserInputs(updatedInputs);
            setEditedCells(updatedEditedCells);

            const { newConflicts, conflictingCells } = validateSudoku(
                updatedInputs,
                puzzleData
            );
            setConflicts(newConflicts);
            setEditedCells(conflictingCells);

            if (newConflicts.size === 0) {
                setMessage("No conflicts found.");
            } else {
                setMessage("Conflicts detected.");
            }
        }
    };

    const solveSudoku = () => {
        if (puzzleData) {
            setUserInputs(puzzleData.solution);
            setEditedCells(new Set());
            setConflicts(new Set());
            setMessage("Sudoku solved.");
        }
    };

    const renderSudokuBoard = () => {
        if (!puzzleData) {
            return <div>Loading...</div>;
        }

        return puzzleData.puzzle.map((row: string[], rowIndex: number) => (
            <div key={`row-${rowIndex}`} className="flex">
                {row.map((value: string, colIndex: number) => {
                    const cellKey = `${rowIndex}-${colIndex}`;
                    const isConflicted = conflicts.has(cellKey);
                    const isEditedConflict = editedCells.has(cellKey);
                    const isInitial = initialCells.has(cellKey);
                    return (
                        <input
                            key={`cell-${rowIndex}-${colIndex}`}
                            className={`w-10 h-10 flex items-center justify-center border text-black ${
                                isConflicted ? "bg-pink-200" : ""
                            } ${
                                value !== "." && !isEditedConflict
                                    ? "text-blue-500"
                                    : userInputs[rowIndex][colIndex] !== "." &&
                                      isEditedConflict
                                    ? "text-red-500"
                                    : ""
                            }`}
                            style={{
                                borderTop:
                                    rowIndex === 0 ? "2px solid black" : "none",
                                borderLeft:
                                    colIndex === 0 ? "2px solid black" : "none",
                                borderBottom:
                                    rowIndex % 3 === 2
                                        ? "2px solid black"
                                        : "1px solid black",
                                borderRight:
                                    colIndex % 3 === 2
                                        ? "2px solid black"
                                        : "1px solid black",
                                fontSize: "16px",
                                fontFamily: "monospace",
                                textAlign: "center",
                            }}
                            type="text"
                            value={
                                userInputs[rowIndex][colIndex] !== "."
                                    ? userInputs[rowIndex][colIndex]
                                    : ""
                            }
                            onChange={(e) =>
                                handleInputChange(
                                    rowIndex,
                                    colIndex,
                                    e.target.value
                                )
                            }
                            maxLength={1}
                            readOnly={isInitial}
                        />
                    );
                })}
            </div>
        ));
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <h1 className="text-2xl font-bold mb-6">Sudoku</h1>
            <p className="mb-6">{message || "Loading..."}</p>
            <div className="mb-6">
                <Button color="primary" onClick={fetchRandomSudoku}>
                    Random
                </Button>
                <Button color="primary" onClick={clearSudokuBoard}>
                    Clear
                </Button>
                <Dropdown>
                    <DropdownTrigger>
                        <Button variant="bordered" color="primary">
                            Select Difficulty
                        </Button>
                    </DropdownTrigger>
                    <DropdownMenu
                        aria-label="Static Actions"
                        onAction={(key) => fetchSudokuByDifficulty(String(key))}
                    >
                        <DropdownItem key="low">Low</DropdownItem>
                        <DropdownItem key="medium">Medium</DropdownItem>
                        <DropdownItem key="high">High</DropdownItem>
                    </DropdownMenu>
                </Dropdown>
            </div>
            <div className="mb-6">
                <Button color="primary" onClick={solveSudoku}>
                    Solve
                </Button>
                <Button
                    color="primary"
                    onClick={(
                        event: React.MouseEvent<HTMLButtonElement, MouseEvent>
                    ) => solveNextStep(userInputs)}
                >
                    Solve Next
                </Button>
            </div>
            <div>{renderSudokuBoard()}</div>
        </main>
    );
}
