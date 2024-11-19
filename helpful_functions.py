import colors as colors
from colorsys import hsv_to_rgb
from math import sqrt, acos, exp
from functools import wraps
import time
from decimal import Decimal
import os
import shutil
import math
import keyboard
from warnings import warn
import sys

clear = "\033c"
defaultTextSpeed = 150 # symbols/second

def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

def time_it( func ):
    """
    Decorator that measures the runtime of the function it decorates.

    Args:
        func: The function to be decorated.

    Returns:
        The wrapper function that measures and prints the execution time.
    """
    @wraps( func )
    def wrapper( *args, **kwargs ):
        start_time = time.time( )  # Record the start time
        result = func( *args, **kwargs )  # Call the original function
        end_time = time.time( )  # Record the end time
        duration = end_time - start_time  # Calculate the duration
        print( f"Function '{func.__name__}' took {duration:.4f} seconds to complete." )
        return result  # Return the original function's result
    return wrapper

def readFile( pName: str, pNr: int | None = None, extension: str = ".txt", split: bool = True ) -> list[str]:
    """
    Reads a file ending with a number, useful when multiple similar files are in use, like different tasks or configs

    Args:
        pName ( String ): Path to the file location and file name
        pNr ( int ): Files number for iterating through similar files
        extension ( String ): Files file extension. Defaults to '.txt'
        removeEmpty ( Boolean ): Toggles wether empty lines are removed.Defaults to True

    Returns:
        Array: array of Strings, each String a line
    """
    if pNr:
        dateiname = pName + str( pNr ) + extension
    else:
        dateiname = pName + extension
    with open( dateiname, "r", encoding = "utf-8" ) as data:
        tmp = data.read( )
        if split: tmp = tmp.split( "\n" )
        ausgabe = []
        for i in tmp:
            if not i == "":
                ausgabe.append( i )
    return ausgabe

def lenformat( pIn: str | int, pLength: int, character: str = " ", place: str = "back" ) -> int:
    """
    Extends the length of a given string or integer to a specified length for prettier terminal output

    Args:
        pIn ( string, int ): The text that is to be formated
        pLength ( int ): Amount of characters the text should occupy in total
        character ( str, optional ): Characters used to fill blank space. Defaults to ' '.
        place ( str, optional ): Defines wether characters should be placed in front or behind text.\n
            Accepts: 
                'front' / 'f'
                'back'  / 'b'  < Default
                'brace' / 'br' / 'center' / 'c'

    Returns:
        String: String, formated
    """
    if len( str( pIn ) ) > pLength:
        warn( "Warning: Input text exceeded desired length.\nText will be shortened to fit within given length" )
        if pLength >= 5:     pIn = pIn [ :pLength - 3 ] + "..."
        else:               pIn = pIn [ :pLength ]
    if place == "back" or place == "b":
        return str( str( pIn ) + str( character * int( int( pLength ) - len( str( pIn ) ) ) ) )
    elif place == "front" or place == "f":
        return str( character * int( int( pLength ) - len( str( pIn ) ) ) ) + str( str( pIn ) )
    elif place == "brace" or place == "br" or place == "center" or place == "c":
        return str( math.floor((pLength - len(pIn)) / 2) * character + str(pIn) + math.ceil((pLength - len(pIn)) / 2) * character)
    else:
        raise SyntaxError ( f"Error: unsupported place type used in 'lenformat': {place}" )
    
def progressBar( percentage: float | int, length: int, empty: str = "-", filled: str = "#", braces: str = "[]" ):
    if braces == " " or braces == "": braces = "  "
    filled_length = int( length * percentage )

    return( braces[ 0 ] + ( filled * filled_length ) + ( empty * ( length - filled_length -1 ) ) + braces[1] )
    
def clearTerminal( ) -> None:
    """
    clears the Terminal
    """
    print( "\033c", end="" )  # Clears Python Console Output

def clearLastTerminalLine( ) -> None:
    print( f"{colors.CURSOR_UP}{colors.CURSOR_ERASE_LINE}",end="" )

def get_terminal_width( ) -> int:
    """Gets the width of the terminal in characters."""
    return os.get_terminal_size( ).columns

def calculate_wrapped_lines( text: str, terminal_width: int ) -> int:
    """
    Calculates how many lines a text will take up in the terminal considering wrapping.
    
    Args:
        text ( str ): The text to be printed.
        terminal_width ( int ): The width of the terminal.
    
    Returns:
        ( int ): The number of lines the text will take up.
    """
    wrapped_lines = wrap_text( text, terminal_width )
    return len( wrapped_lines )

def wrap_text( text: str, width: int ) -> list[str]:
    """
    Wrap the text into a list of lines, ensuring that no line exceeds the terminal width.
    
    Args:
        text ( str ): The text to wrap.
        width ( int ): The maximum width of the terminal.
    
    Returns:
        list[str]: A list of wrapped lines.
    """
    words = text.split( ' ' )
    lines = []
    current_line = ""
    
    for word in words:
        # Add the word to the current line if it fits within the width
        if len( current_line ) + len( word ) + 1 <= width:
            current_line += ( word + ' ' )
        else:
            # If the word doesn't fit, move the current line to the list and start a new line
            lines.append( current_line.strip( ) )
            current_line = word + ' '
    
    # Add the last line if there's remaining text
    if current_line:
        lines.append( current_line.strip( ) )
    
    return lines

def print_wrapped_text( text: str ) -> None:
    """
    Prints the text with manual wrapping to avoid issues with terminal automatic line wrapping.
    
    Args:
        text ( str ): The text to print.
    """
    terminal_width = get_terminal_width( )
    wrapped_lines = wrap_text( text, terminal_width )
    
    for line in wrapped_lines:
        print( line )

def clear_lines( num_lines: int ) -> None:
    """
    Clears the specified number of lines from the terminal output.
    
    Args:
        num_lines ( int ): The number of lines to clear.
    """
    for _ in range( num_lines ):
        print( "\033[F\033[K", end='' )  # Move cursor up and clear the line

def printAnimated(text: str, ttw: float = 1.0, sps: int = 150, mode="ttw", doLineBreak: bool = False) -> None:
    """
    Animates writing of text to the terminal on a single line.

    Args:
        text (str): Text to animate.
        ttw (float, optional): Total Time Waited. Defaults to 1.0.
        sps (int, optional): Symbols per second. Defaults to 150.
        mode (str, optional): Determines the mode. Accepts:
            'sps' (symbols per second)
            'ttw' (total time waited)  < Default
        doLineBreak (bool, optional): Whether to add a line break after text. Defaults to True.
    """
    chars = len(text)

    # Determine wait time per character
    if mode == "sps":
        if sps <= 0:
            raise ValueError(f"Error: sps (symbols per second) must be greater than zero (is {sps})")
        wait = 1 / sps
    elif mode == "ttw":
        if ttw < 0:
            raise ValueError(f"Error: ttw (time to wait) must be greater than or equal zero (is {sps})")
        wait = ttw / chars
    else:
        raise ValueError(f"Error: Unexpected print type ({mode}) while trying to print out text:\n{text}")

    enterBlock: bool = False
    if keyboard.is_pressed("enter"): enterBlock = True
    for i in text:
        # Clear the current line, return to the start of the line, and print updated text
        print(i, end="", flush= True)  # Clear line from cursor to end, then print up to current character
        for _ in range(int(float(wait) / 0.01)):  # Check every 0.01 seconds
            if keyboard.is_pressed("space") or (keyboard.is_pressed("enter") and not enterBlock):  # Replace "any_key" with the desired key
                sys.stdout.write("\r\033[K" + text)  # Immediately print full text
                sys.stdout.flush()
                return
            time.sleep(0.01)
        if enterBlock:
                if not keyboard.is_pressed("enter"): enterBlock = False

    # Optionally add a new line after the animated text
    if doLineBreak:
        print()  # Use print() here to add a single line break after the text

def makeMatrix( 
        pX: int, 
        pY: int, 
        pZ:int =1
        ) -> list:
    """
    Easy way to quickly generate empty matrix
    Args:
        pX ( int ): matrix x dimension
        pY ( int ): matrix y dimension
        pY ( int ): matrix z dimension.\n
            Defaults to 1

    Returns:
        matrix ( array ): 2-Dimensional, empty data matrix
    """
    ret = []
    for i in range ( pY ):
        ret.append( [] )
        for j in range( pX ):
            ret[i].append( [] )
            if pZ > 1:
                for n in range( pZ ):
                    ret[i][j].append( [] )  
    return ret

def transpose(matrix):
    """
    Transposes the given matrix (rows become columns and vice versa).

    Parameters:
    matrix (list of lists): The matrix to be transposed.

    Returns:
    list of lists: The transposed matrix.
    """
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError("Input must be a list of lists")
    return [list(row) for row in zip(*matrix)]

def HSVpercentToRGB( 
        H: float, 
        saturation: float = 100, 
        value: float = 100
        ) -> tuple[ float, float, float ]:
    """
    Gibt den RGB-Wert basierend auf dem Prozentsatz durch den Hue-Wert zurück.
    Args:
        percentage ( int ): Ein Prozentsatz ( 0 bis 100 ), der angibt, wie weit man durch den Hue-Wert fortgeschritten ist.
    Returns:
        RBG ( tupel ): Ein Tupel ( R, G, B ) mit den RGB-Werten.
    """
    if not ( 0 <= H <= 100 ):
        raise ValueError( "Percentage must be between 0 and 100" )
    hue = ( H / 100.0 ) * 360
    hue_normalized = hue / 360.0
    r, g, b = hsv_to_rgb( hue_normalized, saturation/100, value/100 )
    
    return ( float( r * 255 ), float( g * 255 ), float( b * 255 ) )

def RGBtoKivyColorCode( color: tuple ) -> tuple[ float, float, float ]:
    """
    | Converts a color from standart RGB color space to Kivy color space,
    | which is clamped between ```0-1``` instead of the normal ```0-25```

    Args:
        colorRGB  ( tuple ): Takes a ```0 - 255``` RBG Tupel ```( R, G, B )```
    Returns:
        colorKivy ( tuple ): returns same color value in Kivy color space
    """
    return( float( color[ 0 ] / 255 ), float( color[ 1 ] / 255 ), float( color[ 2 ] / 255 ) )

def normalizeVector( vector: tuple ) -> tuple:
    """
    Normalizes a given *n*-dimensional vector\n
    .. math:: ∥V∥ = sqrt( v^( 2/1 ) + v^( 2/2 ) + ⋯ + v^( 2/n ) )

    Args:
        vector ( tuple ): *n*-dimensional vector

    Raises:
        ValueError: does not accept zero vector

    Returns:
        tuple: normalized vector
    """
    # Calculate the magnitude of the vector
    magnitude = sqrt( sum( v**2 for v in vector ) )
    
    # Avoid division by zero
    if magnitude == 0:
        raise ValueError( "Cannot normalize a zero vector" )
    
    # Divide each component by the magnitude
    return [v / magnitude for v in vector]

def vector_add( v1, v2 ):
    """
    Adds two vectors element-wise.

    Parameters:
    v1 ( list ): The first vector.
    v2 ( list ): The second vector.

    Returns:
    list: The resulting vector after addition.
    """
    return [a + b for a, b in zip( v1, v2 )]

def vector_subtract( v1, v2 ):
    """
    Subtracts the second vector from the first vector element-wise.

    Parameters:
    v1 ( list ): The first vector.
    v2 ( list ): The second vector.

    Returns:
    list: The resulting vector after subtraction.
    """
    return [a - b for a, b in zip( v1, v2 )]

def doesLineIntersect(p1: tuple[float, float], p2: tuple[float, float], vec: tuple[float, float], dir: tuple[float, float]) -> bool:
    """
    Check if the vector originating at `vec` in the direction `dir` intersects
    the line segment from `p1` to `p2`.

    Parameters:
    p1 (tuple): Start point of the line segment.
    p2 (tuple): End point of the line segment.
    vec (tuple): Starting point of the vector.
    dir (tuple): Direction vector.

    Returns:
    bool: True if the vector intersects the line segment, False otherwise.
    """
    # Line segment vector
    line_vec = (p2[0] - p1[0], p2[1] - p1[1])
    
    # Determinant to check if lines are parallel
    det = dir[0] * line_vec[1] - dir[1] * line_vec[0]
    if det == 0:
        return False  # Lines are parallel and do not intersect

    # Parameter t for the vector line
    t = ((p1[0] - vec[0]) * line_vec[1] - (p1[1] - vec[1]) * line_vec[0]) / det
    # Parameter u for the line segment
    u = ((vec[0] - p1[0]) * dir[1] - (vec[1] - p1[1]) * dir[0]) / det
    
    # Debugging output
    print(f"det: {det}, t: {t}, u: {u}")
    
    # Check if u is within [0, 1] (within the segment) and t >= 0 (forward direction)
    return 0 <= u <= 1 and t >= 0

def lineIntersection(p1: tuple[float, float], p2: tuple[float, float], q1: tuple[float, float], q2: tuple[float, float]) -> tuple[float, float] | None:
    """
    Calculate the intersection point of two lines if they intersect.

    Parameters:
    p1 (tuple): Start point of the first line.
    p2 (tuple): End point of the first line.
    q1 (tuple): Start point of the second line.
    q2 (tuple): End point of the second line.

    Returns:
    tuple[float, float] | None: The intersection point as (x, y), or None if lines are parallel.
    """
    # Line vectors
    r = (p2[0] - p1[0], p2[1] - p1[1])
    s = (q2[0] - q1[0], q2[1] - q1[1])

    # Determinant
    det = r[0] * s[1] - r[1] * s[0]
    if det == 0:
        return None  # Lines are parallel or coincident

    # Parameters for the lines
    t = ((q1[0] - p1[0]) * s[1] - (q1[1] - p1[1]) * s[0]) / det
    u = ((q1[0] - p1[0]) * r[1] - (q1[1] - p1[1]) * r[0]) / det

    # Calculate intersection point
    intersect_x = p1[0] + t * r[0]
    intersect_y = p1[1] + t * r[1]
    
    return (intersect_x, intersect_y) if 0 <= t <= 1 and 0 <= u <= 1 else None

def dot( v1, v2 ):
    return sum( x * y for x, y in zip( v1, v2 ) )

def dot2( vector1, vector2 ):
    """
    Calculate the dot product of two 2D vectors.
    
    Parameters:
    vector1: list or tuple of 2 elements ( x1, y1 )
    vector2: list or tuple of 2 elements ( x2, y2 )
    
    Returns:
    The dot product of the two vectors.
    """
    if len( vector1 ) != 2 or len( vector2 ) != 2:
        raise ValueError( "Both vectors must have exactly 2 elements." )
    
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def dot3( vector1, vector2 ):
    """
    Calculate the dot product of two 3D vectors.
    
    Parameters:
    vector1: list or tuple of 3 elements ( x1, y1, z1 )
    vector2: list or tuple of 3 elements ( x2, y2, z2 )
    
    Returns:
    The dot product of the two vectors.
    """
    if len( vector1 ) != 3 or len( vector2 ) != 3:
        raise ValueError( "Both vectors must have exactly 3 elements." )
    
    return vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]

def scalar_vector_mult( scalar, vector ):
    """
    Multiplies a scalar with each element of the vector.

    Parameters:
    scalar ( float or int ): The scalar value.
    vector ( list or array ): The vector with which the scalar is multiplied.

    Returns:
    list: A new vector resulting from the scalar-vector multiplication.
    """
    return [scalar * element for element in vector]

def mag3( vector ):
    """
    Calculate the magnitude of a 3D vector.
    
    Parameters:
    vector: list or tuple of 3 elements ( x, y, z )
    
    Returns:
    The magnitude of the vector.
    """
    return sqrt( vector[0]**2 + vector[1]**2 + vector[2]**2 )

def mag2( vector ):
    """
    Calculate the magnitude of a 2D vector.
    
    Parameters:
    vector: list or tuple of 3 elements ( x, y )
    
    Returns:
    The magnitude of the vector.
    """
    return sqrt( vector[0]**2 + vector[1]**2 )

def vec2angleRad( vector1, vector2 ):
    """
    Calculate the angle between two 2D vectors in radians.
    
    Parameters:
    vector1: list or tuple of 2 elements ( x1, y1 )
    vector2: list or tuple of 2 elements ( x2, y2 )
    
    Returns:
    The angle between the two vectors in radians.
    """
    dot_prod = dot2( vector1, vector2 )
    magnitude_v1 = mag2( vector1 )
    magnitude_v2 = mag2( vector2 )
    
    # Calculate cosine of the angle using the dot product formula
    cos_angle = dot_prod / ( magnitude_v1 * magnitude_v2 )
    
    # To avoid floating point inaccuracies, ensure the value is in the range [-1, 1]
    cos_angle = max( min( cos_angle, 1 ), -1 )
    
    # Calculate the angle in radians
    angle_radians = acos( cos_angle )
    
    return angle_radians

def vec3angleRad( vector1, vector2 ):
    """
    Calculate the angle between two 3D vectors in radians.
    
    Parameters:
    vector1: list or tuple of 3 elements ( x1, y1, z1 )
    vector2: list or tuple of 3 elements ( x2, y2, z2 )
    
    Returns:
    The angle between the two vectors in degrees.
    """
    dot_prod = dot3( vector1, vector2 )
    magnitude_v1 = mag3( vector1 )
    magnitude_v2 = mag3( vector2 )
    
    # Calculate cosine of the angle using the dot product formula
    cos_angle = dot_prod / ( magnitude_v1 * magnitude_v2 )
    
    # To avoid floating point inaccuracies, ensure the value is in the range [-1, 1]
    cos_angle = max( min( cos_angle, 1 ), -1 )
    
    # Calculate the angle in radians
    angle_radians = acos( cos_angle )
    
    return angle_radians

def timeFormat( seconds: int | float ) -> str:
    # Extract days, hours, minutes, seconds, and milliseconds
    days = int( seconds // 86400 )
    seconds %= 86400
    hours = int( seconds // 3600 )
    seconds %= 3600
    minutes = int( seconds // 60 )
    seconds %= 60
    milliseconds = int( ( seconds - int( seconds ) ) * 1000 )
    seconds = int( seconds )

    # Format the output as dd:hh:mm:ss:msms
    return f"{days:02}d {hours:02}h {minutes:02}m {seconds:02}s {milliseconds:03}ms"
