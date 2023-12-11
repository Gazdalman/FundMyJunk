const SecondCategory = (
  setSecondCat,
  secondCat,
  secondSubcat,
  setSecondSubcat) => {
  return (
    <div id="second-cat-form">
      <div id="second-cat-info">
        <h2>Second Category</h2>
        <div id="second-category-description">
          <p>This doesn't really matter. Don't ask me why it's here! Ask the moron who built the site! Oh...</p>
        </div>
      </div>
      <div id="second-cat-fields">
        <span id="second-cat-input">
          <label id="second-cat-label">Second Category</label>
          <select
          className="input-field"
            value={secondCat}
            onChange={(e) => setSecondCat(e.target.value)}
          >
            <option value="">Not for now</option>
          </select>
        </span>
        <span id="second-subcat-input">
          <label id="second-subcat-label">Second SubCategory</label>
          <select
          className="input-field"
            value={secondSubcat}
            onChange={(e) => setSecondSubcat(e.target.value)}
          >
            <option value="">Not for now</option>
          </select>
        </span>
      </div>
    </div>
  )
}

export default SecondCategory
