import Data.List.Split

readStr :: IO [String]
readStr = splitOn "," <$> getContents

pStr :: [String] -> [(String, String)]
pStr inp =
  let lStr = map (splitOn "-") inp
   in map (\x -> (head x, (head . tail) x)) lStr

isInvalid :: String -> Bool
isInvalid str = not (head str == '0' || start == end)
  where
    (start, end) = splitAt (div (length str) 2) str

walkRange :: (String, String) -> Int -> Int
walkRange (s1, e1) state = sum [a | a <- [s2 .. e2], not . isInvalid . show $ a]
  where
    (s2, e2) = (read s1 :: Int, read e1 :: Int)

main :: IO () = do
  io <- readStr
  let inp = pStr io
  print $ sum $ map (`walkRange` 0) inp
