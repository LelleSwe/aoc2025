listMax :: (Ord a) => [a] -> (Int, a)
listMax [x] = (0, x)
listMax (x : xs)
  | max (snd prev) x == x = (0, x)
  | otherwise = (fst prev + 1, snd prev)
  where
    prev = listMax xs

findLargest :: (Int, Char) -> String -> (Int, Char)
findLargest (idxBig, big) = listMax . drop (idxBig + 1)

lineSol :: String -> Int
lineSol inp = read $ snd s1 : [snd s2]
  where
    s1 = listMax $ reverse . drop 1 . reverse $ inp
    s2 = findLargest s1 inp

readlinesStr :: IO [String]
readlinesStr = lines <$> getContents

main :: IO () = do
  io <- readlinesStr
  print $ sum $ map lineSol io
