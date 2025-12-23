readlinesStr :: IO [String]
readlinesStr = lines <$> getContents

-- True for right rotation
rot :: String -> (Int, Int)
rot s = (a, b)
 where
  a = if 'R' == head s then 1 else -1
  b = read $ tail s

walkStart :: [(Int, Int)] -> Int
walkStart = fst . walk (0, 50)

walk :: (Int, Int) -> [(Int, Int)] -> (Int, Int)
walk start [] = start
walk start ((r, mov) : xs) = walk next2 xs
 where
  next = (r * mov + snd start) `mod` 100
  next2 =
    if next == 0
      then
        (fst start + 1, next)
      else
        (fst start, next)

main :: IO () = do
  io <- readlinesStr
  print $ walkStart $ map rot io
