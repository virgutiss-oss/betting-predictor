import Foundation
import Combine

class MatchViewModel: ObservableObject {
    @Published var matches: [Match] = []
    
    func loadMatches() {
        let githubURL = "https://raw.githubusercontent.com/TAVO_USERNAME/TAVO_REPO/main/stats/matches.json"
        GitHubService.shared.fetchMatches(from: githubURL) { [weak self] matches in
            self?.matches = matches
        }
    }
    
    func winProbability(for match: Match) -> Double {
        let totalOdds = match.odds1 + match.odds2
        return (match.odds2 / totalOdds) * 100
    }
}
