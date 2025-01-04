import "./Counter.scss";
import CountUp from "react-countup";
import { useInView } from "react-intersection-observer";

const Counter = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.5,
  });

  return (
    <section ref={ref} className="counter">
      {inView && (
        <div className="counter__box">
          <CountUp end={9443} duration={3} className="counter__number" />
          <p className="counter__text">Happy Customers</p>
        </div>
      )}
      {inView && (
        <div className="counter__box">
          <CountUp end={342} duration={4} className="counter__number" />
          <p className="counter__text">Products Available</p>
        </div>
      )}
      {inView && (
        <div className="counter__box">
          <CountUp end={95} duration={4} className="counter__number" />
          <p className="counter__text">Tech Experts</p>
        </div>
      )}
      {inView && (
        <div className="counter__box">
          <CountUp end={15} duration={4} className="counter__number" />
          <p className="counter__text">Years of Excellence</p>
        </div>
      )}
    </section>
  );
};

export default Counter;
