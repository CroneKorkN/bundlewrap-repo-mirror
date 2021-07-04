from(bucket: "${bucket}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["host"] == "${host}")
% for key, value in filters.items():
  |> filter(fn: (r) => r["${key}"] == "${value}")
% endfor
  |> filter(fn: (r) => r["_field"] == "${field}")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
