import { Link } from "react-router-dom";

const VideoItem = ({ title, url, thumbnail }) => {
  return (
    <div className="pricing__box">
      <img src={thumbnail} alt={title} className="pricing__thumbnail" />
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="pricing__content">
        <h3 className="pricing__box-title">{title}</h3>
        <button className="pricing__link">Watch Video</button>
      </a>
    </div>
  );
};

export default VideoItem;
