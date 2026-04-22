export class ExplanationService {
  generate({ trustScore, riskLevel, signals }) {
    const strongestSignal = Object.entries(signals).sort((a, b) => b[1] - a[1])[0];
    const weakestSignal = Object.entries(signals).sort((a, b) => a[1] - b[1])[0];

    return `This score is ${trustScore}/100 (${riskLevel}) because ${strongestSignal[0]} is strongest at ${strongestSignal[1]}, while ${weakestSignal[0]} is weakest at ${weakestSignal[1]}.`;
  }
}
