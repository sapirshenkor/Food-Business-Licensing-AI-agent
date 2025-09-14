import React, { useState } from "react";
import { businessLicensingAPI } from "../../services/api";

const SurveyForm = ({ onSurveyComplete }) => {
  // Form state
  const [formData, setFormData] = useState({
    size: "",
    max_people: "",
    uses_gas: false,
    has_delivery: false,
    serves_meat: false,
    business_name: "",
    location: "",
  });

  // UI state
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  // Form validation
  const validateForm = () => {
    const newErrors = {};

    if (!formData.size || formData.size < 10) {
      newErrors.size = 'גודל העסק חייב להיות לפחות 10 מ"ר';
    }
    if (formData.size > 10000) {
      newErrors.size = 'גודל העסק לא יכול להיות יותר מ-10,000 מ"ר';
    }
    if (!formData.max_people || formData.max_people < 1) {
      newErrors.max_people = "מספר המקומות חייב להיות לפחות 1";
    }
    if (formData.max_people > 1000) {
      newErrors.max_people = "מספר המקומות לא יכול להיות יותר מ-1,000";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Convert strings to numbers
      const surveyData = {
        ...formData,
        size: parseFloat(formData.size),
        max_people: parseInt(formData.max_people),
      };

      console.log("📝 Submitting survey:", surveyData);

      const result = await businessLicensingAPI.submitSurvey(surveyData);

      if (result.success) {
        onSurveyComplete(result.data);
      } else {
        setErrors({ submit: result.error });
      }
    } catch (error) {
      console.error("Survey submission error:", error);
      setErrors({ submit: "שגיאה בשליחת הטופס. נסה שוב." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="survey-form">
      <div className="form-header">
        <h2>📋 פרטי העסק שלך</h2>
        <p>מלא את הפרטים ונכין לך דוח רישוי מותאם אישית</p>
      </div>

      <form onSubmit={handleSubmit} className="survey-form-content">
        {/* Business Name (Optional) */}
        <div className="form-group">
          <label htmlFor="business_name">🏢 שם העסק (אופציונלי)</label>
          <input
            type="text"
            id="business_name"
            name="business_name"
            value={formData.business_name}
            onChange={handleInputChange}
            placeholder="לדוגמה: מסעדת הפלאפל"
            className="form-input"
          />
        </div>

        {/* Business Size */}
        <div className="form-group">
          <label htmlFor="size">📏 גודל העסק במ"ר *</label>
          <input
            type="number"
            id="size"
            name="size"
            value={formData.size}
            onChange={handleInputChange}
            placeholder="לדוגמה: 80"
            className={`form-input ${errors.size ? "error" : ""}`}
            min="10"
            max="10000"
            required
          />
          {errors.size && <span className="error-message">{errors.size}</span>}
        </div>

        {/* Max People */}
        <div className="form-group">
          <label htmlFor="max_people">👥 מספר מקומות ישיבה מקסימלי *</label>
          <input
            type="number"
            id="max_people"
            name="max_people"
            value={formData.max_people}
            onChange={handleInputChange}
            placeholder="לדוגמה: 50"
            className={`form-input ${errors.max_people ? "error" : ""}`}
            min="1"
            max="1000"
            required
          />
          {errors.max_people && (
            <span className="error-message">{errors.max_people}</span>
          )}
        </div>

        {/* Location (Optional) */}
        <div className="form-group">
          <label htmlFor="location">📍 מיקום העסק (אופציונלי)</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="לדוגמה: תל אביב"
            className="form-input"
          />
        </div>

        {/* Special Features */}
        <div className="form-group features-group">
          <label className="features-title">🎯 מאפיינים מיוחדים</label>
          <p className="features-subtitle">
            בחר את המאפיינים הרלוונטיים לעסק שלך:
          </p>

          <div className="features-grid">
            {/* Gas Usage */}
            <div className="feature-item">
              <label className="feature-label">
                <input
                  type="checkbox"
                  name="uses_gas"
                  checked={formData.uses_gas}
                  onChange={handleInputChange}
                  className="feature-checkbox"
                />
                <span className="feature-text">
                  <span className="feature-icon">🔥</span>
                  <span className="feature-name">שימוש בגז</span>
                  <span className="feature-desc">המסעדה משתמשת בגז לבישול</span>
                </span>
              </label>
            </div>

            {/* Delivery */}
            <div className="feature-item">
              <label className="feature-label">
                <input
                  type="checkbox"
                  name="has_delivery"
                  checked={formData.has_delivery}
                  onChange={handleInputChange}
                  className="feature-checkbox"
                />
                <span className="feature-text">
                  <span className="feature-icon">🚚</span>
                  <span className="feature-name">משלוחים</span>
                  <span className="feature-desc">שירות משלוחי מזון</span>
                </span>
              </label>
            </div>

            {/* Meat Serving */}
            <div className="feature-item">
              <label className="feature-label">
                <input
                  type="checkbox"
                  name="serves_meat"
                  checked={formData.serves_meat}
                  onChange={handleInputChange}
                  className="feature-checkbox"
                />
                <span className="feature-text">
                  <span className="feature-icon">🥩</span>
                  <span className="feature-name">הגשת בשר</span>
                  <span className="feature-desc">המסעדה מגישה מנות בשר</span>
                </span>
              </label>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="form-group">
          {errors.submit && (
            <div className="error-message submit-error">{errors.submit}</div>
          )}

          <button
            type="submit"
            className={`submit-button ${loading ? "loading" : ""}`}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="loading-spinner">⏳</span>
                מכין דוח...
              </>
            ) : (
              <>
                <span className="button-icon">🚀</span>
                צור דוח רישוי
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SurveyForm;
