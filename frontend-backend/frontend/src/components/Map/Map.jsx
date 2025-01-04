import "./Map.scss";

const Map = () => {
  return (
    <div className="map">
      <iframe
        className="map__frame"
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2562.5074701729813!2d21.95900727606486!3d50.02750857104152!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x473cfbdc8dc0b313%3A0x7a9e0987f3b6a1c!2sUniversity%20of%20Rzeszow!5e0!3m2!1sen!2spl!4v1696409486045!5m2!1sen!2spl"
        width="600"
        height="450"
        allowFullScreen=""
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
        title="University of Rzeszów"></iframe>
    </div>
  );
};

export default Map;
