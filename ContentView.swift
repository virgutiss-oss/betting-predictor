import SwiftUI
import Charts

struct ContentView: View {
    @StateObject var viewModel = MatchViewModel()
    
    var body: some View {
        NavigationView {
            List(viewModel.matches) { match in
                VStack(alignment: .leading) {
                    Text("\(match.team1) vs \(match.team2)")
                        .font(.headline)
                    
                    HStack {
                        Text("Odds: \(match.odds1, specifier: "%.2f") - \(match.odds2, specifier: "%.2f")")
                        Spacer()
                        Text("Win %: \(viewModel.winProbability(for: match), specifier: "%.1f")%")
                            .bold()
                    }
                    
                    Text("Result: \(match.result)")
                        .foregroundColor(match.result == match.team1 ? .green : .red)
                }
                .padding(.vertical, 5)
            }
            .navigationTitle("Statymų analizė")
            .onAppear {
                viewModel.loadMatches()
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
