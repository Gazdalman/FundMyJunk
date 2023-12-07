import { useEffect, useState } from "react"
import PhotoField from "../utilities/PhotoField";

const RewardItemForm = ({ setItems, items, setItemData, itemData, setItemForm, itemForm, index, setIndex }) => {
  const [title, setTitle] = useState("")
  const [focused, setFocused] = useState("");
  const [disabled, setDisabled] = useState(true)
  const [quantity, setQuantity] = useState("")
  const [image, setImage] = useState("")
  const [imageURL, setImageURL] = useState("")

  const handleFocus = (field) => {
    setFocused(field);
  };

  const handleBlur = (field) => {
    setFocused("");
    if (field == "quantity") {
      setQuantity(quantity ? Math.round(quantity) : 1)
    }
  };

  const showItemForm = (e) => {
    e.preventDefault()
    setItemForm(false)
  }

  const addItem = async (e) => {
    e.preventDefault()
    const newItemData = new FormData()
    if (image) newItemData.append("image", image)
    newItemData.append("quantity", quantity)
    newItemData.append("title", title)

    const item = {
      index,
      title,
      image,
      quantity
    }

    const newIDObj = {...itemData}
    newIDObj[index] = newItemData
    const newItems = {...items}
    newItems[index] = item
    setItems({...newItems})
    setItemData({...newIDObj})
    setIndex(index+1)
    setItemForm(false)
  }

  useEffect(() => {
    if (quantity > 9999999) {
      setQuantity(9999999)
    }
  },[quantity])

  return (
    <div id="reward-item-input-div">
      <form id="reward-item-form" onSubmit={addItem} encType="multipart/form-data">
        <div className={`item-title-field floating-input ${focused == "title" ? 'focused' : ''}`}>
          <label className={`itf-label input-label ${focused == "title" || title ? 'label-focus' : ''}`}>
            Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onFocus={(e) => handleFocus("title", e)}
            onBlur={handleBlur}
            className="rtf-input input-field"
          />
        </div>
        <div className={`item-quantity-field floating-input ${focused == "quantity" ? 'focused' : ''}`}>
          <label className={`iqf-label input-label ${focused == "quantity" || quantity ? 'label-focus' : ''}`}>
            Quantity
          </label>
          <input
            type="number"
            value={quantity}
            max="9999999"
            onChange={(e) => setQuantity(e.target.value)}
            onFocus={(e) => handleFocus("quantity", e)}
            onBlur={handleBlur}
            className="rqf-input input-field"
          />
        </div>
        (Image is optional for item)
        <PhotoField
          extraClass={"item-form-image"}
          image={image}
          setImage={setImage}
          setImageURL={setImageURL}
          imageURL={imageURL}
        />
        <button id="hide-item-form" onClick={showItemForm}>Cancel</button>
        <button disabled={title.length < 3 || !quantity} id="save-item">Add Item</button>
      </form>
    </div>
  )
}

export default RewardItemForm
