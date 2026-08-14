function sortItems(items, field) {
  return items.sort((a, b) => a[field] > b[field] ? 1 : -1);
}
// bug: string comparison on numeric fields like 'price'
