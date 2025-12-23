import Data.List.Split

readlines :: IO [String]
readlines = lines <$> getContents

toPoint :: String -> (Int, Int)
toPoint s =
  let split = splitOn "," s
   in (read . head $ split, read . head . tail $ split)

-- den här mannen tänkte på förra bruh
-- dist :: (Int, Int) -> (Int, Int) -> Double
-- dist (px, py) (qx, qy) = sqrt . fromIntegral $ (px - qx) ^ 2 + (py - qy) ^ 2

area :: (Int, Int) -> (Int, Int) -> Int
area (px, py) (qx, qy) = (px - qx + 1) * (py - qy + 1)

bruteOne :: (Int, Int) -> [(Int, Int)] -> Int
bruteOne p [] = 0
bruteOne p1 (p2 : ps) = max (area p1 p2) (bruteOne p1 ps)

sol :: [(Int, Int)] -> Int
sol inp = foldl max 0 $ map (`bruteOne` inp) inp

main :: IO () = do
  io <- readlines
  let points = map toPoint io
  print $ sol points
