import { FaMapLocationDot, FaPhoneVolume } from "react-icons/fa6";
import { LuMails } from "react-icons/lu";

const boxData = [
  {
    id: 1,
    link: "https://www.google.com/maps/d/viewer?mid=1Ukx7g7T7p0beMiNitKmOHSjMH25YDbT2&femb=1&ll=50.028049243218305%2C21.955955222535536&z=13", // Google Maps link to University of Rzeszów
    icon: <FaMapLocationDot />,
    boxTitle: "Address",
    details: "University of Rzeszów, Rejtana 16C, 35-959 Rzeszów, Poland",
    target: "_blank",
  },
  {
    id: 2,
    link: "tel:+48177872100", // University of Rzeszów phone number
    icon: <FaPhoneVolume />,
    boxTitle: "Call Us",
    details: "+48 17 787 21 00",
  },
  {
    id: 3,
    link: "mailto:info@ur.edu.pl", // University of Rzeszów email address
    icon: <LuMails />,
    boxTitle: "Email Us",
    details: "info@ur.edu.pl",
  },
];

export default boxData;
