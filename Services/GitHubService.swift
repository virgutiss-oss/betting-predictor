import Foundation
import Combine

class GitHubService {
    static let shared = GitHubService()
    
    private init() {}
    
    func fetchMatches(from urlString: String, completion: @escaping ([Match]) -> Void) {
        guard let url = URL(string: urlString) else { return }
        
        var request = URLRequest(url: url)
        // Jei repo privatus, įrašyk savo GitHub Personal Access Token čia:
        // request.addValue("token TAVO_PERSONAL_ACCESS_TOKEN", forHTTPHeaderField: "Authorization")
        
        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let matches = try JSONDecoder().decode([Match].self, from: data)
                    DispatchQueue.main.async {
                        completion(matches)
                    }
                } catch {
                    print("Decoding error: \(error)")
                    DispatchQueue.main.async { completion([]) }
                }
            }
        }.resume()
    }
}
