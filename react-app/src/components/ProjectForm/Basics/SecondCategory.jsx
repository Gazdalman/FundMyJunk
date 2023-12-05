const SecondCategory = (
  setSecondCat,
  secondCat,
  secondSubcat,
  setSecondSubcat) => {
  return (
    <div id="second-cat-form">
      <span id="second-cat-input">
        <label>Second Category</label>
        <select
          value={secondCat}
          onChange={(e) => setSecondCat(e.target.value)}
        >
          <option value="">Not for now</option>
        </select>
      </span>
      <span id="second-cat-input">
        <label>Second SubCategory</label>
        <select
          value={secondSubcat}
          onChange={(e) => setSecondSubcat(e.target.value)}
        >
          <option value="">Not for now</option>
        </select>
      </span>
    </div>
  )
}

export default SecondCategory
