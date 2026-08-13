import { Link } from "react-router-dom";

export default function PerformerDetailPage({ performer }) {
  return (
    <div>
      <h1>{performer.name}</h1>
      {/* BUG: clicking the rank badge goes to a generic leaderboard,
          not this performer's own page. Should link to
          /performers/${performer.id} */}
      <a href="/leaderboard">5-star</a>
    </div>
  );
}
