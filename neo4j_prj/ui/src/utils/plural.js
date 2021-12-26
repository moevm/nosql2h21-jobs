export function plural(n, variants) {
  if (n % 10 === 1 && n % 100 !== 11) {
    return variants[0];
  }

  if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) {
    return variants[1];
  }

  return variants[2];
}
