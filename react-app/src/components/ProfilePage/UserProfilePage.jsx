import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux";
import { getSingleUser } from "../../store/session";
import { useParams, useHistory } from "react-router-dom";

const UserProfilePage = () => {
  const { id } = useParams()
  const dispatch = useDispatch()
  const history = useHistory()
  const pageUser = useSelector(state => state.session.requestedUser);
  const currUser = useSelector(state => state.session.user);
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    if (currUser && currUser.id == id) {
      return history.push("/profile")
    }
    dispatch(getSingleUser(id))
    setIsLoaded(true)
  }, [dispatch])

  return isLoaded && pageUser? (
    <div id="user-profile-container">
      <h1 id="user-display-name">{pageUser.displayName}</h1>
    </div>
  ) : null
}

export default UserProfilePage
