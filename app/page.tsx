"use client";

import { useCallback, useEffect, useState } from "react";
import {
    Button,
    Dropdown,
    DropdownItem,
    DropdownMenu,
    DropdownTrigger,
} from "@nextui-org/react";
import { SudokuData } from "./types/index";
import { validateSudoku } from "./components/validateSudoku";
import { defaultPuzzle } from "./components/defaultData";

const apiBaseUrl = (process.env.NEXT_PUBLIC_API_BASE_URL || "/api").replace(
    /\/$/,
    ""
);

const isBoard = (value: unknown): value is string[][] =>
    Array.isArray(value) &&
    value.length === 9 &&
    value.every(
        (row) =>
            Array.isArray(row) &&
            row.length === 9 &&
            row.every(
                (cell) =>
                    typeof cell === "string" && /^(\.|[1-9])$/.test(cell)
            )
    );

async function responseError(response: Response): Promise<string> {
    try {
        const body = await response.json();
        if (typeof body.detail === "string") {
            return body.detail;
        }
    } catch {
        // Use the status fallback below for non-JSON responses.
    }
    return `Request failed (${response.status}).`;
}

export default function Home() {
    const [message, setMessage] = useState("Loading...");
    const [puzzleData, setPuzzleData] = useState<SudokuData | null>(null);
    const [userInputs, setUserInputs] = useState<string[][]>([]);
    const [conflicts, setConflicts] = useState<Set<string>>(new Set());
    const [initialCells, setInitialCells] = useState<Set<string>>(new Set());
    const [isLoading, setIsLoading] = useState(false);

    const loadPuzzle = useCallback((data: SudokuData, loadedMessage: string) => {
        if (!isBoard(data.puzzle)) {
            throw new Error("The server returned an invalid puzzle.");
        }

        const puzzle = data.puzzle.map((row) => row.slice());
        const initial = new Set<string>();
        puzzle.forEach((row, rowIndex) =>
            row.forEach((cell, colIndex) => {
                if (cell !== ".") {
                    initial.add(`${rowIndex}-${colIndex}`);
                }
            })
        );

        setPuzzleData({ ...data, puzzle });
        setUserInputs(puzzle);
        setInitialCells(initial);
        setConflicts(new Set());
        setMessage(loadedMessage);
    }, []);

    const fetchPuzzle = async (path: string, loadedMessage: string) => {
        setIsLoading(true);
        setMessage("Loading puzzle...");
        try {
            const response = await fetch(`${apiBaseUrl}${path}`);
            if (!response.ok) {
                throw new Error(await responseError(response));
            }
            loadPuzzle(await response.json(), loadedMessage);
        } catch (error) {
            setMessage(
                error instanceof Error ? error.message : "Failed to load puzzle."
            );
        } finally {
            setIsLoading(false);
        }
    };

    const submitBoard = async (path: string, successMessage: string) => {
        if (conflicts.size > 0) {
            setMessage("Resolve conflicting values before solving.");
            return;
        }

        setIsLoading(true);
        setMessage("Solving...");
        try {
            const response = await fetch(`${apiBaseUrl}${path}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ puzzle: userInputs }),
            });
            if (!response.ok) {
                throw new Error(await responseError(response));
            }

            const data: { puzzle?: unknown } = await response.json();
            if (!isBoard(data.puzzle)) {
                throw new Error("The server returned an invalid solution.");
            }

            const result = data.puzzle.map((row) => row.slice());
            setUserInputs(result);
            setPuzzleData((current) =>
                current ? { ...current, puzzle: result } : current
            );
            setConflicts(new Set());
            setMessage(successMessage);
        } catch (error) {
            setMessage(
                error instanceof Error ? error.message : "Failed to solve puzzle."
            );
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        const initial =
            defaultPuzzle[Math.floor(Math.random() * defaultPuzzle.length)];
        loadPuzzle(initial, "Puzzle loaded");
    }, [loadPuzzle]);

    const clearSudokuBoard = () => {
        const emptyBoard = Array.from({ length: 9 }, () => Array(9).fill("."));
        loadPuzzle(
            {
                id: 0,
                puzzle: emptyBoard,
                solution: emptyBoard.map((row) => row.slice()),
                clues: 0,
                difficulty: "none",
            },
            "Board cleared"
        );
    };

    const handleInputChange = (
        rowIndex: number,
        colIndex: number,
        value: string
    ) => {
        if (value !== "" && !/^[1-9]$/.test(value)) {
            setMessage("Enter a digit from 1 to 9.");
            return;
        }

        const updatedInputs = userInputs.map((row, currentRow) =>
            row.map((cell, currentCol) =>
                currentRow === rowIndex && currentCol === colIndex
                    ? value || "."
                    : cell
            )
        );
        setUserInputs(updatedInputs);

        const { newConflicts } = validateSudoku(updatedInputs, puzzleData);
        setConflicts(newConflicts);
        setMessage(
            newConflicts.size === 0
                ? "No conflicts found."
                : "Conflicting values detected."
        );
    };

    const renderSudokuBoard = () => {
        if (!puzzleData || userInputs.length !== 9) {
            return <div>Loading...</div>;
        }

        return userInputs.map((row, rowIndex) => (
            <div key={`row-${rowIndex}`} className="flex">
                {row.map((value, colIndex) => {
                    const cellKey = `${rowIndex}-${colIndex}`;
                    const isConflicted = conflicts.has(cellKey);
                    const isInitial = initialCells.has(cellKey);
                    return (
                        <input
                            key={`cell-${rowIndex}-${colIndex}`}
                            aria-label={`Row ${rowIndex + 1}, column ${
                                colIndex + 1
                            }`}
                            aria-invalid={isConflicted}
                            className={`w-10 h-10 border text-black ${
                                isConflicted
                                    ? "bg-pink-200 text-red-700"
                                    : isInitial
                                    ? "text-blue-500"
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
                            inputMode="numeric"
                            value={value === "." ? "" : value}
                            onChange={(event) =>
                                handleInputChange(
                                    rowIndex,
                                    colIndex,
                                    event.target.value
                                )
                            }
                            maxLength={1}
                            readOnly={isInitial}
                            disabled={isLoading}
                        />
                    );
                })}
            </div>
        ));
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <h1 className="text-2xl font-bold mb-6">Sudoku</h1>
            <p className="mb-6" role="status">
                {message}
            </p>
            <div className="mb-6">
                <Button
                    color="primary"
                    isDisabled={isLoading}
                    onClick={() =>
                        fetchPuzzle(
                            "/python/get_randomsudoku",
                            "Puzzle loaded"
                        )
                    }
                >
                    Random
                </Button>
                <Button
                    color="primary"
                    isDisabled={isLoading}
                    onClick={clearSudokuBoard}
                >
                    Clear
                </Button>
                <Dropdown>
                    <DropdownTrigger>
                        <Button
                            variant="bordered"
                            color="primary"
                            isDisabled={isLoading}
                        >
                            Select Difficulty
                        </Button>
                    </DropdownTrigger>
                    <DropdownMenu
                        aria-label="Select puzzle difficulty"
                        onAction={(key) =>
                            fetchPuzzle(
                                `/python/sudoku/difficulty/${String(key)}`,
                                `Puzzle loaded with difficulty: ${String(key)}`
                            )
                        }
                    >
                        <DropdownItem key="low">Low</DropdownItem>
                        <DropdownItem key="medium">Medium</DropdownItem>
                        <DropdownItem key="high">High</DropdownItem>
                    </DropdownMenu>
                </Dropdown>
            </div>
            <div className="mb-6">
                <Button
                    color="primary"
                    isDisabled={isLoading}
                    onClick={() =>
                        submitBoard("/python/solve", "Sudoku solved.")
                    }
                >
                    Solve
                </Button>
                <Button
                    color="primary"
                    isDisabled={isLoading}
                    onClick={() =>
                        submitBoard(
                            "/python/solve_next_step",
                            "Puzzle step solved."
                        )
                    }
                >
                    Solve Next
                </Button>
            </div>
            <div>{renderSudokuBoard()}</div>
        </main>
    );
}
