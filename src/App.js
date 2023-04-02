import React, { Component } from "react";
import Plot from "react-plotly.js";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ticker: "",
      predictedData: null,
      error: null,
    };
    this.handleTickerChange = this.handleTickerChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleTickerChange(event) {
    this.setState({ ticker: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ticker: this.state.ticker }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        this.setState({ predictedData: data.predictedData, error: null });
      })
      .catch((error) => {
        console.error("Error:", error);
        this.setState({ predictedData: null, error: error.message });
      });
  }

  render() {
    const { ticker, predictedData, error } = this.state;

    return (
      <div className="App">
        <form onSubmit={this.handleSubmit}>
          <input
            type="text"
            value={ticker}
            onChange={this.handleTickerChange}
          />
          <button type="submit">Predict</button>
        </form>
        {error && <p>{error}</p>}
        {predictedData && (
          <Plot
            data={[
              {
                x: predictedData.map((d) => d.date),
                y: predictedData.map((d) => d.price),
                type: "scatter",
              },
            ]}
            layout={{ title: `Predicted Prices for ${ticker}` }}
          />
        )}
      </div>
    );
  }
}

export default App;
