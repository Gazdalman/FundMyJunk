import { useState } from "react";

const MainCategory = ({ mainCategory, mainSubcat, setMainCategory, setMainSubcat}) => {
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleBlur = () => {
    setIsFocused(false);
  };

  return (
    <div className={`floating-input ${isFocused ? 'focused' : ''}`}>
      <label className={`input-label ${isFocused || mainCategory ? 'label-focus' : ''}`}>
        Category
      </label>
      <input
        type="text"
        value={mainCategory}
        onChange={(e) => setMainCategory(e.target.value)}
        onFocus={handleFocus}
        onBlur={handleBlur}
        className="input-field"
      />
    </div>
  );
}

export default MainCategory
