/**
 * Base abstraction for all signal providers.
 * Concrete implementations must return a score between 0 and 100.
 */
export class BaseSignalService {
  constructor(signalName) {
    this.signalName = signalName;
  }

  async analyze(_input) {
    throw new Error(`${this.signalName} analyze() must be implemented`);
  }
}
