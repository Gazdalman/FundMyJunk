import { useState } from "react";

const MainCategory = ({ mainCategory, mainSubcat, setMainCategory, setMainSubcat }) => {

  return (
    <div id="main-cat-form">
      <span id="main-cat-input">
        <label>Main Category</label>
        <select
          value={mainCategory}
          onChange={(e) => {
            setMainSubcat("")
            setMainCategory(e.target.value)
          }}
        >
          <option value="">--Select--</option>
          <option value="Art">Just gonna say 'Art' for now</option>
        </select>
      </span>
      <span id="main-cat-input">
        <label>Main SubCategory</label>
        <select
        disabled={!mainCategory}
          value={mainSubcat}
          onChange={(e) => setMainSubcat(e.target.value)}
        >
          <option value="">--Select--</option>
          <option value="Ceramics">Just gonna say 'Ceramics' for now</option>
        </select>
      </span>
    </div>
  );
}

export default MainCategory
