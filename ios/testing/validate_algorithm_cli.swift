#!/usr/bin/env swift
//
// validate_algorithm_cli.swift
// Command-line tool for validating algorithms using iOS cube engine
//
// Usage:
//   swift validate_algorithm_cli.swift <case_code> <algorithm_sequence>
//
// Output: JSON with validation result
//

import Foundation

// This script needs to be run in the context of the Xcode project to access DeddalCore
// For now, create a simple JSON output that Python can parse

struct ValidationResult: Codable {
    let isValid: Bool
    let error: String?
    let caseCode: String
    let algorithm: String

    enum ValidationError: String {
        case empty = "Algorithm is empty"
        case invalidNotation = "Invalid move notation"
        case doesNotSolve = "Algorithm doesn't solve the case"
        case caseNotFound = "Case not found"
        case suboptimal = "Algorithm has suboptimal move patterns"
        case duplicate = "Algorithm already exists"
    }
}

// Simple move validation (matches iOS MoveSequence pattern)
func validateMoveNotation(_ sequence: String) -> (Bool, String?) {
    let trimmed = sequence.trimmingCharacters(in: .whitespacesAndNewlines)

    guard !trimmed.isEmpty else {
        return (false, "empty")
    }

    let moves = trimmed.split(separator: " ")
    let validMovePattern = try! NSRegularExpression(pattern: "^[RUFLDBMESxyzrufldб]['2]?$")

    for move in moves {
        let moveStr = String(move)
        let range = NSRange(moveStr.startIndex..., in: moveStr)

        if validMovePattern.firstMatch(in: moveStr, range: range) == nil {
            return (false, "invalidNotation:\(moveStr)")
        }
    }

    return (true, nil)
}

// Main
guard CommandLine.arguments.count >= 3 else {
    let usage = """
    Usage: swift validate_algorithm_cli.swift <case_code> <algorithm_sequence>

    Example:
      swift validate_algorithm_cli.swift "3X3-CFOP-OLL-24" "R U R' U'"
    """
    print(usage)
    exit(1)
}

let caseCode = CommandLine.arguments[1]
let algorithm = CommandLine.arguments[2]

// Validate move notation
let (isValid, error) = validateMoveNotation(algorithm)

let result = ValidationResult(
    isValid: isValid,
    error: error,
    caseCode: caseCode,
    algorithm: algorithm
)

// Output JSON
let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted

if let jsonData = try? encoder.encode(result),
   let jsonString = String(data: jsonData, encoding: .utf8) {
    print(jsonString)
} else {
    print("""
    {
      "isValid": false,
      "error": "encoding_error",
      "caseCode": "\(caseCode)",
      "algorithm": "\(algorithm)"
    }
    """)
}
