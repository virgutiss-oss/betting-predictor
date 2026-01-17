import Foundation

struct Match: Codable, Identifiable {
    let id = UUID()
    let team1: String
    let team2: String
    let odds1: Double
    let odds2: Double
    let result: String
}
