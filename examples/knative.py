"""
Simple Lithops example using the map method.
In this example the map() method will launch one
map function for each entry in 'iterdata'. Finally
it will print the results for each invocation with
pw.get_result()
"""
import lithops


def my_function(id, x):
    print("I'm activation number {}".format(id))
    return x + 7


if __name__ == '__main__':
    iterdata = [1, 2, 3, 4]
    pw = lithops.knative_executor()
    pw.map(my_function, iterdata)
    print(pw.get_result())
