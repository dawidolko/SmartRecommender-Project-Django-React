import "./NotFound.scss";
import { useEffect } from "react";
import { FaRegFaceFrown } from "react-icons/fa6";
import { useNavigate } from "react-router-dom";

const NotFound = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timeout = setTimeout(() => {
      navigate("/");
    }, 5000);

    return () => clearTimeout(timeout); // Cleanup timeout on unmount
  }, [navigate]);

  return (
    <section className="notFound">
      <FaRegFaceFrown className="notFound__icon" />
      <p className="notFound__error">404</p>
      <h2 className="notFound__title">Page Not Found</h2>
      <p className="notFound__text">
        Sorry, the page you're looking for doesn't exist. You will be redirected
        to the homepage shortly.
      </p>
    </section>
  );
};

export default NotFound;
