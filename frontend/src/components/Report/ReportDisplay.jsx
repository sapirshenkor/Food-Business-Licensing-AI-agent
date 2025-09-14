import React, { useState } from "react";
import ReactMarkdown from "react-markdown";

const ReportDisplay = ({ surveyResult, onNewSurvey }) => {
  const {
    survey_data,
    personalized_report,
    requirements_count,
    estimated_total_cost,
    estimated_total_time,
  } = surveyResult;

  return (
    <div className="report-display">
      {/* Report Header */}
      <div className="report-header">
        <h2>🎉 הדוח שלך מוכן!</h2>
        <p>נוצר דוח מותאם אישית עבור העסק שלך</p>
      </div>

      {/* Quick Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card">
          <div className="card-icon">📋</div>
          <div className="card-content">
            <div className="card-number">{requirements_count}</div>
            <div className="card-label">רישיונות נדרשים</div>
          </div>
        </div>
      </div>

      {/* Business Details Summary */}
      <div className="business-summary">
        <h3>📊 פרטי העסק שהוזנו:</h3>
        <div className="business-details">
          <span>📏 גודל: {survey_data.size} מ"ר</span>
          <span>👥 תפוסה: {survey_data.max_people} מקומות</span>
          {survey_data.uses_gas && <span>🔥 שימוש בגז</span>}
          {survey_data.has_delivery && <span>🚚 משלוחים</span>}
          {survey_data.serves_meat && <span>🥩 הגשת בשר</span>}
        </div>
      </div>

      {/* Main Report Content */}
      <div className="report-content">
        <h3>📋 הדוח המלא:</h3>
        <div className="markdown-content">
          <ReactMarkdown>{personalized_report}</ReactMarkdown>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="report-actions">
        {/* New Survey Button */}
        <button onClick={onNewSurvey} className="new-survey-btn">
          🔄 צור דוח חדש
        </button>
      </div>

      {/* Debug Info (Optional - remove in production) */}
      <div className="debug-section">
        <details>
          <summary>🔍 מידע טכני (לפיתוח)</summary>
          <pre>
            {JSON.stringify(
              {
                requirements_count,
                estimated_total_cost,
                estimated_total_time,
              },
              null,
              2
            )}
          </pre>
        </details>
      </div>
    </div>
  );
};

export default ReportDisplay;
