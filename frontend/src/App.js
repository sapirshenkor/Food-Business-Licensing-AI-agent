import React, { useState } from "react";
import "./App.css";
import SurveyForm from "./components/Survey/SurveyForm";
import ReportDisplay from "./components/Report/ReportDisplay";
import "./components/Survey/SurveyForm.css";
import "./components/Report/ReportDisplay.css";

function App() {
  const [surveyResult, setSurveyResult] = useState(null);

  const handleSurveyComplete = (result) => {
    console.log("📊 Survey completed:", result);
    setSurveyResult(result);
  };

  const handleNewSurvey = () => {
    setSurveyResult(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏢 Business Licensing AI</h1>
        <p>מערכת AI לרישוי עסקים בישראל</p>
      </header>

      <main className="App-main">
        {!surveyResult ? (
          <SurveyForm onSurveyComplete={handleSurveyComplete} />
        ) : (
          <ReportDisplay
            surveyResult={surveyResult}
            onNewSurvey={handleNewSurvey}
          />
        )}
      </main>
    </div>
  );
}

export default App;
