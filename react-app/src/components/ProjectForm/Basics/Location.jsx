import { useState } from "react";

const Location = ({ location, setLocation }) => {
  const [isFocused, setIsFocused] = useState(false);
  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleBlur = () => {
    setIsFocused(false);
  };

  return (
    <div className={`floating-input ${isFocused ? 'focused' : ''}`}>
      <label className={`input-label ${isFocused || location ? 'label-focus' : ''}`}>
        Location
      </label>
      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        onFocus={handleFocus}
        onBlur={handleBlur}
        className="input-field"
      />
    </div>
  )
}

export default Location
