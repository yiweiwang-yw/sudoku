"use client";

import { useEffect, useState } from "react";
interface SudokuData {
    id: number;
    puzzle: string[][];
    solution: string[][];
    clues: number;
    difficulty: string;
}

export default function Home() {
    const [message, setMessage] = useState<string>("");
    const [puzzleData, setPuzzleData] = useState<SudokuData | null>(null);

    async function fetchRandomSudoku() {
        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/python/randomsudoku"
            );
            const data: SudokuData = await response.json();
            setMessage("Puzzle loaded");
            setPuzzleData(data);
            console.log("data", data)
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    useEffect(() => {
        fetchRandomSudoku();
    }, []);

    // Function to render the Sudoku board cells
    const renderSudokuBoard = () => {
        if (!puzzleData) {
            return <div>Loading...</div>;
        }

        return puzzleData.puzzle.map((row: string[], rowIndex: number) => (
            <div key={`row-${rowIndex}`} className="flex">
                {row.map((value: string, colIndex: number) => (
                    <div
                        key={`cell-${rowIndex}-${colIndex}`}
                        className={`w-10 h-10 flex items-center justify-center border ${
                            rowIndex % 3 === 2 && colIndex % 3 === 2
                                ? "border-b-2 border-r-2"
                                : ""
                        } ${rowIndex === 8 ? "border-b-2" : ""} ${
                            colIndex === 8 ? "border-r-2" : ""
                        }`}
                        style={{
                            borderTop: rowIndex === 0 ? "2px solid" : "none",
                            borderLeft: colIndex === 0 ? "2px solid" : "none",
                            borderBottom:
                                rowIndex % 3 === 2 ? "2px solid" : "1px solid",
                            borderRight:
                                colIndex % 3 === 2 ? "2px solid" : "1px solid",
                            fontSize: "16px",
                            fontFamily: "monospace",
                        }}
                    >
                        {value !== "." ? value : ""}
                    </div>
                ))}
            </div>
        ));
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <h1 className="text-2xl font-bold mb-6">Home Page</h1>
            <p className="mb-6">{message || "Loading..."}</p>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full mb-5" onClick={fetchRandomSudoku}>
                Random
            </button>
            <div>{renderSudokuBoard()}</div>
        </main>
    );
}
