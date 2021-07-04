from(bucket: "${bucket}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
% for key, values in filters.items():
<% values = values if isinstance(values, list) else [values] %>\
  |> filter(fn: (r) => ${' or '.join(f'r["{key}"] == "{value}"' for value in values)})
% endfor
% if function == 'derivative':
  |> derivative()
% else:
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
% endif
  |> yield(name: "mean")
