def prime_table(n):
  l = [True for _ in xrange(n+1)]
  i = 2
  while i * i <= n:
    if l[i]:
      j = i + i
      while j <= n:
        l[j] = False
        j += i
    i += 1

  table = [i for i in xrange(n+1) if l[i] and i>=2]
  return table
