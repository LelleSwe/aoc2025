listMax :: String -> (Int, Char)
listMax (x : xs)
  | null xs = (0, x)
  | max (snd prev) x == x = (0, x)
  | otherwise = (fst prev + 1, snd prev)
  where
    prev = listMax xs

loopOver :: Int -> String -> String
loopOver current inp
  | current == 0 = ""
  | otherwise = snd next : nextLoop
  where
    next = listMax $ reverse . drop (current - 1) . reverse $ inp
    nextLoop = loopOver (current - 1) $ drop (fst next + 1) inp

lineSol :: String -> Int
lineSol = read . loopOver 12

readlinesStr :: IO [String]
readlinesStr = lines <$> getContents

main :: IO () = do
  io <- readlinesStr
  print $ sum $ map lineSol io
