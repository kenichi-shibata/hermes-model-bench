// Grid page - lazy loads 60 at a time via "Load more". This is
// WORKING AS INTENDED (red herring, not a bug) despite looking slow
// on a 2700-performer dataset.
export default function PerformersGrid({ performers }) {
  return <div>{performers.slice(0, 60).map(p => <div key={p.id}>{p.name}</div>)}</div>;
}
