"use client";

import { useEffect, useState } from "react";
import {
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownItem,
    Button,
} from "@nextui-org/react";

interface SudokuData {
    id: number;
    puzzle: string[][];
    solution: string[][];
    clues: number;
    difficulty: string;
}

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export default function Home() {
    const [message, setMessage] = useState<string>("");
    const [puzzleData, setPuzzleData] = useState<SudokuData | null>(null);
    const [userInputs, setUserInputs] = useState<string[][]>([]);
    const [editedCells, setEditedCells] = useState<Set<string>>(new Set());

    async function fetchRandomSudoku() {
        try {
            const response = await fetch(
                `${apiBaseUrl}/python/get_randomsudoku`
            );
            const data: SudokuData = await response.json();
            setMessage("Puzzle loaded");
            setPuzzleData(data);
            setUserInputs(data.puzzle.map((row) => row.slice()));
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    async function fetchSudokuByDifficulty(difficulty: any) {
        try {
            const response = await fetch(
                `${apiBaseUrl}/python/sudoku/difficulty/${difficulty}`
            );
            const data: SudokuData = await response.json();
            setMessage(`Puzzle loaded with difficulty: ${difficulty}`);
            setPuzzleData(data);
            setUserInputs(data.puzzle.map((row) => row.slice()));
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    useEffect(() => {
        setPuzzleData(initializeEmptyBoard());
    }, []);

    const initializeEmptyBoard = () => {
        const emptyBoard = Array.from({ length: 9 }, () => Array(9).fill("."));
        setUserInputs(emptyBoard);
        setEditedCells(new Set());
        setMessage("Board initialized");
        return {
            id: 0,
            puzzle: emptyBoard,
            solution: emptyBoard,
            clues: 0,
            difficulty: "none",
        };
    };

    const clearSudokuBoard = () => {
        setPuzzleData(initializeEmptyBoard());
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
        }
    };

    const renderSudokuBoard = () => {
        if (!puzzleData) {
            return <div>Loading...</div>;
        }

        return puzzleData.puzzle.map((row: string[], rowIndex: number) => (
            <div key={`row-${rowIndex}`} className="flex">
                {row.map((value: string, colIndex: number) => (
                    <input
                        key={`cell-${rowIndex}-${colIndex}`}
                        className={`w-10 h-10 flex items-center justify-center border text-black ${
                            value !== "." &&
                            !editedCells.has(`${rowIndex}-${colIndex}`)
                                ? "text-blue-500"
                                : userInputs[rowIndex][colIndex] !== "."
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
                    />
                ))}
            </div>
        ));
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <h1 className="text-2xl font-bold mb-6">Home Page</h1>
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
            <div>{renderSudokuBoard()}</div>
        </main>
    );
}
