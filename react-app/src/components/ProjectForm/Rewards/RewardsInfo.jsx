import { useEffect, useState } from "react"
import PhotoField from "../utilities/PhotoField";
import { useHistory, useParams } from "react-router-dom";
import RewardItemForm from "./RewardItem";
import { useDispatch } from "react-redux";
import { createReward } from "../../../store/project";

const RewardInfo = () => {
  const dispatch = useDispatch()
  const history = useHistory();
  const [focused, setFocused] = useState("");
  const [disabled, setDisabled] = useState(true);
  const { projectId } = useParams()
  const [index, setIndex] = useState(1)
  const [selectedIndex, setSelectedIndex] = useState("")
  const [rewardTitle, setRewardTitle] = useState("")
  const [itemForm, setItemForm] = useState(false)
  const [selectedShipping, setSelectedShipping] = useState("");
  const [selectedQuantity, setSelectedQuantity] = useState("")
  const [selectedItem, setSelectedItem] = useState("")
  const [amount, setAmount] = useState("")
  const [image, setImage] = useState("")
  const [imageURL, setImageURL] = useState("")
  const [description, setDescription] = useState("")
  const [items, setItems] = useState([])
  const [itemData, setItemData] = useState([])
  const [physicalItems, setPhysicalItems] = useState(false)
  const [deliveryDate, setDeliveryDate] = useState("")
  const [shipping, setShipping] = useState("")
  const [unlimited, setUnlimited] = useState(false)
  const [quantity, setQuantity] = useState("")
  const today = new Date().toISOString().split("T")[0];

  const handleFocus = (field) => {
    setFocused(field);
  };

  const handleBlur = (field) => {
    setFocused("");
    if (field == "quantity") {
      setQuantity(quantity ? Math.round(quantity) : 1)
    }
  };

  const handleItemChange = (e) => {
    setPhysicalItems(e.target.value)
    setSelectedItem(e.target.value)
    setShipping("")
    setSelectedShipping("")
  }

  const handleShippingChange = (e) => {
    setShipping(e.target.value)
    setSelectedShipping(e.target.value);
  };

  const handleQuantityChange = (e) => {
    setUnlimited(e.target.value)
    setSelectedQuantity(e.target.value);
  };

  const changeDate = () => {
    const selectedDate = new Date(deliveryDate ? deliveryDate : today);

    // Extract month and year
    const month = selectedDate.toLocaleString('default', { month: 'long' });
    const year = selectedDate.getFullYear();
    return `${month} ${year}`
  }

  const showItemForm = (e) => {
    e.preventDefault()
    setItemForm(true)
  }

  const deleteItem = (key, e) => {
    e.preventDefault()
    const newItems = {...items}
    const newItemData = {...itemData}
    delete newItems[key]
    delete newItemData[key]
    setItems({...newItems})
    setItemData({...newItemData})
  }

  const handleRewardSubmit = async (e) => {
    e.preventDefault()

    const rewardData = new FormData()
    rewardData.append("title", rewardTitle)
    rewardData.append("image", image)
    rewardData.append("amount", amount)
    if (description) rewardData.append("description", description)
    rewardData.append("physicalItems", physicalItems)
    rewardData.append("unlimited", unlimited)
    rewardData.append("deliveryDate", deliveryDate)
    if (quantity) rewardData.append("quantity", quantity)
    rewardData.append("shipping", shipping)

    const res = await dispatch(createReward(rewardData, Object.values(itemData), projectId))
  }

  useEffect(() => {
    if (rewardTitle.length > 3 &&
      image &&
      shipping &&
      deliveryDate &&
      amount
    ) {
      setDisabled(false)
    } else {
      setDisabled(true)
    }

    if (description && description.length < 10) {
      setDisabled(true)
    }

  })

  return !itemForm ? (
    <div id="reward-form-div">
      <div id="reward-input-container">
        <form id="reward-form" onSubmit={handleRewardSubmit} encType="multipart/form-data">
          <h1 id="reward-form-header">Add a Reward</h1>
          <div className={`reward-title-field floating-input ${focused == "title" ? 'focused' : ''}`}>
            <label className={`rtf-label input-label ${focused == "title" || rewardTitle ? 'label-focus' : ''}`}>
              Title
            </label>
            <input
              type="text"
              value={rewardTitle}
              onChange={(e) => setRewardTitle(e.target.value)}
              onFocus={(e) => handleFocus("title", e)}
              onBlur={handleBlur}
              className="rtf-input input-field"
            />
          </div>
          <div className={`reward-amount-field floating-input ${focused == "amount" ? 'focused' : ''}`}>
            <label className={`raf-label input-label ${focused == "amount" || amount ? 'label-focus' : ''}`}>
              Amount
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              onFocus={() => handleFocus("amount")}
              onBlur={handleBlur}
              className="raf-input input-field"
            />
          </div>
          <div id="reward-dnd-box">
            <PhotoField
              image={image}
              setImage={setImage}
              setImageURL={setImageURL}
              imageURL={imageURL}
            />
          </div>
          <div id="add-item-div">
            <h4>Items</h4>
            {Object.values(items) && Object.values(items).map((item) => (
              <>
              <span >{item.quantity ? `${item.quantity}x` : ""} {item.title}</span>
              <button onClick={(e) => deleteItem(item.index, e)} id="edit-item-form">Remove Item</button>
              </>
            ))}
            <button id="show-item-form" onClick={showItemForm}>Add Item</button>

          </div>
          <div className={`reward-description-field floating-input ${focused == "description" ? 'focused' : ''}`}>
            <label className={`rdf-label input-label ${focused == "description" || description ? 'label-focus' : ''}`}>
              Description
            </label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              onFocus={() => handleFocus("description")}
              onBlur={handleBlur}
              className="rdf-input input-field"
            />
          </div>
          <div id="physical-items">
            <label>
              <input
                value="true"
                type="radio"
                checked={selectedItem == "true"}
                onChange={handleItemChange}
              />
              Physical Items
            </label>
            <label>
              <input
                value="false"
                type="radio"
                checked={selectedItem == "false"}
                onChange={handleItemChange}
              />
              Digital Goods Only
            </label>
          </div>
          <div id="shipping-radio">
            <label className="shipping-option">
              <input
                disabled={selectedItem == "false"}
                type="radio"
                value="Ships to anywhere"
                checked={selectedShipping === "Ships to anywhere"}
                onChange={handleShippingChange}
              />
              Ships to anywhere in the world
            </label>
            <label className="shipping-option">
              <input
                disabled={selectedItem == "false"}
                type="radio"
                value="Local event"
                checked={selectedShipping === "Local event"}
                onChange={handleShippingChange}
              />
              Local pickup (not sketchy AT ALL), event, or service (no shipping)
            </label>
            <label className="shipping-option">
              <input
                disabled={selectedItem == "true"}
                type="radio"
                value="Digital rewards"
                checked={selectedShipping === "Digital rewards"}
                onChange={handleShippingChange}
              />
              Digital Reward (no shipping)
            </label>
          </div>
          {selectedShipping && <input
            value={deliveryDate}
            type="date"
            min={today}
            onChange={(e) => setDeliveryDate(e.target.value)}
            className="input-field"
          />}
          <div id="quantity-input-field">
            <label>
              <input
                value="unlimited"
                type="radio"
                checked={selectedQuantity === "unlimited"}
                onChange={handleQuantityChange}
              />
              Unlimited
            </label>
            <label>
              <input
                value="limited"
                type="radio"
                checked={selectedQuantity === "limited"}
                onChange={handleQuantityChange}
              />
              Limited
            </label>
          </div>
          {selectedQuantity == "limited" &&
            <div className={`reward-quantity-field floating-input ${focused == "quantity" ? 'focused' : ''}`}>
              <label className={`rqf-label input-label ${focused == "quantity" || quantity != "" ? 'label-focus' : ''}`}>
                Quantity
              </label>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                onFocus={() => handleFocus("quantity")}
                onBlur={() => handleBlur("quantity")}
                className="rqf-input input-field"
              />
            </div>
          }
          <div id="reward-preview-div">
            <div id="reward-preview">
              <div id="preview-image">
                <img src={imageURL} />
              </div>
              <div id="preview-mid">
                <h3>Pledge ${amount ? amount : 1} or more</h3>
                <h4>{rewardTitle ? rewardTitle : "Totally Legit Project Title Here"}</h4>
                <h5>{description ? description : "This is where the description of your pyramid scheme will go."}</h5>
                <h6>Includes:</h6>
                <ul>
                  {Object.values(items).length > 0 ? Object.values(items).map(item => (
                    <h6 key={item.title}>
                      <li>{item.quantity > 1 ? `${item.quantity}x` : ""} {item.title}</li>
                    </h6>
                  )) : <h5>No items listed</h5>
                  }
                </ul>
                <h6>ESTIMATED DELIVERY</h6>
                <h5>{changeDate()}</h5>
                <h6>REWARD QUANTITY</h6>
                <h5>{selectedQuantity == "unlimited" ? "Unlimited" : (quantity ? Math.round(quantity) : 1)}</h5>
              </div>
            </div>
          </div>
          <button disabled={disabled} >Add Reward</button>
        </form>
      </div>
    </div >

  ) : <RewardItemForm
  setItems={setItems}
  items={items}
  setItemData={setItemData}
  itemData={itemData}
  setItemForm={setItemForm}
  itemForm={itemForm}
  index={index}
  setIndex={setIndex}
  />
}

export default RewardInfo
