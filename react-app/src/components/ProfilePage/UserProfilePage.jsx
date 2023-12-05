import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux";
import { getSingleUser } from "../../store/session";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

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
    <h1>{pageUser.id}</h1>
    // <h1>fsadf</h1>
  ) : null
}

export default UserProfilePage
