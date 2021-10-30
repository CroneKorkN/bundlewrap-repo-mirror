from(bucket: "${bucket}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
% for key, values in filters.items():
<% values = values if isinstance(values, list) else [values] %>\
  |> filter(fn: (r) => ${' or '.join(f'r["{key}"] == "{value}"' for value in values)})
% endfor
% if function == 'derivative':
  |> derivative(nonNegative: true)
% endif
% if boolean_to_int:
  |> map(fn: (r) => ({r with _value: if r._value == true then 1 else 0 }))
% endif
  |> aggregateWindow(every: duration(v: int(v: v.windowPeriod)*${resolution}), fn: mean, createEmpty: false)
% if negative:
  |> map(fn: (r) => ({r with _value: r._value * - 1.0}))
% endif
  |> yield(name: "mean")
