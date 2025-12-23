import Data.List.Split

readStr :: IO [String]
readStr = splitOn "," <$> getContents

pStr :: [String] -> [(String, String)]
pStr inp =
  let lStr = map (splitOn "-") inp
   in map (\x -> (head x, (head . tail) x)) lStr

allEqual :: [String] -> Bool
allEqual [] = True
allEqual (x : xs) = all (== x) xs

isInvalid :: Int -> String -> Bool
isInvalid int str = ret
  where
    len = allEqual $ chunksOf int str
    ret
      | int > length str `div` 2 = True
      | head str == '0' || len = False
      | otherwise = isInvalid (int + 1) str

walkRange :: (String, String) -> Int -> Int
walkRange (s1, e1) state = sum [a | a <- [s2 .. e2], not . isInvalid 1 . show $ a]
  where
    (s2, e2) = (read s1 :: Int, read e1 :: Int)

main :: IO () = do
  io <- readStr
  let inp = pStr io
  print $ sum $ map (`walkRange` 0) inp
