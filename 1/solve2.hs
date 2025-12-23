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
    preMod = r * mov + snd start
    next2 = (next, preMod `mod` 100)
    next = fst start + down preMod + up preMod + if snd start == 0 && r == -1 then -1 else 0

-- why debug modulo not work when can be stupid
down :: Int -> Int
down x = if x <= 0 then 1 + down (x + 100) else 0

up :: Int -> Int
up x = if x > 99 then 1 + up (x - 100) else 0

main :: IO () = do
  io <- readlinesStr
  print $ walkStart $ map rot io
