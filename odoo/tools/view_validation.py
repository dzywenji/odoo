""" View validation code (using assertions, not the RNG schema). """

import ast
import collections
import logging
import os
import re

from lxml import etree
from odoo import tools

_logger = logging.getLogger(__name__)


_validators = collections.defaultdict(list)
_relaxng_cache = {}

READONLY = re.compile(r"\breadonly\b")


def _get_attrs_symbols():
    """ Return a set of predefined symbols for evaluating attrs. """
    return {
        'True', 'False', 'None',    # those are identifiers in Python 2.7
        'self',
        'id',
        'uid',
        'context',
        'context_today',
        'active_id',
        'active_ids',
        'allowed_company_ids',
        'current_company_id',
        'active_model',
        'time',
        'datetime',
        'relativedelta',
        'current_date',
        'abs',
        'len',
        'bool',
        'float',
        'str',
        'unicode',
    }


def get_variable_names(expr):
    """ Return the subexpressions of the kind "VARNAME(.ATTNAME)*" in the given
    string or AST node.
    """
    IGNORED = _get_attrs_symbols()
    names = set()

    def get_name_seq(node):
        if isinstance(node, ast.Name):
            return [node.id]
        elif isinstance(node, ast.Attribute):
            left = get_name_seq(node.value)
            return left and left + [node.attr]

    def process(node):
        seq = get_name_seq(node)
        if seq and seq[0] not in IGNORED:
            names.add('.'.join(seq))
        else:
            for child in ast.iter_child_nodes(node):
                process(child)

    if isinstance(expr, str):
        expr = ast.parse(expr.strip(), mode='eval').body
    process(expr)

    return names


def get_dict_asts(expr):
    """ Check that the given string or AST node represents a dict expression
    where all keys are string literals, and return it as a dict mapping string
    keys to the AST of values.
    """
    if isinstance(expr, str):
        expr = ast.parse(expr.strip(), mode='eval').body

    if not isinstance(expr, ast.Dict):
        raise ValueError("Non-dict expression")
    if not all(isinstance(key, ast.Str) for key in expr.keys):
        raise ValueError("Non-string literal dict key")
    return {key.s: val for key, val in zip(expr.keys, expr.values)}


def _check(condition, explanation):
    if not condition:
        raise ValueError("Expression is not a valid domain: %s" % explanation)


def get_domain_identifiers(expr):
    """ Check that the given string or AST node represents a domain expression,
    and return a pair of sets ``(fields, vars)`` where ``fields`` are the field
    names on the left-hand side of conditions, and ``vars`` are the variable
    names on the right-hand side of conditions.
    """
    if not expr:  # case of expr=""
        return (set(), set())
    if isinstance(expr, str):
        expr = ast.parse(expr.strip(), mode='eval').body

    fnames = set()
    vnames = set()

    if isinstance(expr, ast.List):
        for elem in expr.elts:
            if isinstance(elem, ast.Str):
                # note: this doesn't check the and/or structure
                _check(elem.s in ('&', '|', '!'),
                       f"logical operators should be '&', '|', or '!', found {elem.s!r}")
                continue

            if not isinstance(elem, (ast.List, ast.Tuple)):
                continue

            _check(len(elem.elts) == 3,
                   f"segments should have 3 elements, found {len(elem.elts)}")
            lhs, operator, rhs = elem.elts
            _check(isinstance(operator, ast.Str),
                   f"operator should be a string, found {type(operator).__name__}")
            if isinstance(lhs, ast.Str):
                fnames.add(lhs.s)

    vnames.update(get_variable_names(expr))

    return (fnames, vnames)


def valid_view(arch, **kwargs):
    for pred in _validators[arch.tag]:
        check = pred(arch, **kwargs)
        if not check:
            _logger.error("Invalid XML: %s", pred.__doc__)
            return False
        if check == "Warning":
            _logger.warning("Invalid XML: %s", pred.__doc__)
            return "Warning"
    return True


def validate(*view_types):
    """ Registers a view-validation function for the specific view types
    """
    def decorator(fn):
        for arch in view_types:
            _validators[arch].append(fn)
        return fn
    return decorator


def relaxng(view_type):
    """ Return a validator for the given view type, or None. """
    if view_type not in _relaxng_cache:
        with tools.file_open(os.path.join('base', 'rng', '%s_view.rng' % view_type)) as frng:
            try:
                relaxng_doc = etree.parse(frng)
                _relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
            except Exception:
                _logger.exception('Failed to load RelaxNG XML schema for views validation')
                _relaxng_cache[view_type] = None
    return _relaxng_cache[view_type]


@validate('calendar', 'graph', 'pivot', 'search', 'tree', 'activity')
def schema_valid(arch, **kwargs):
    """ Get RNG validator and validate RNG file."""
    validator = relaxng(arch.tag)
    if validator and not validator.validate(arch):
        result = True
        for error in validator.error_log:
            _logger.error(tools.ustr(error))
            result = False
        return result
    return True
<<<<<<< HEAD


@validate('search')
def valid_searchpanel(arch, **kwargs):
    """ There must be at most one ``searchpanel`` node in search view archs. """
    return len(arch.xpath('/search/searchpanel')) <= 1


@validate('search')
def valid_searchpanel_domain_select(arch, **kwargs):
    """ In the searchpanel, the attribute ``domain`` can only be used on ``field`` nodes with
        ``select`` attribute set to ``multi``. """
    for child in arch.xpath('/search/searchpanel/field'):
        if child.get('domain') and child.get('select') != 'multi':
            return False
    return True


@validate('search')
def valid_searchpanel_domain_fields(arch, **kwargs):
    """ In the searchpanel, fields used in the ``domain`` attribute must be present inside the
        ``searchpanel`` node with ``select`` attribute not set to ``multi``. """
    searchpanel = arch.xpath('/search/searchpanel')
    if searchpanel:
        env = kwargs['env']
        model = kwargs['model']
        attrs_fields = [r[0] for r in get_attrs_field_names(env, searchpanel[0], env[model], False)]
        non_multi_fields = [
            c.get('name') for c in arch.xpath('/search/searchpanel/field')
            if c.get('select') != 'multi'
        ]
        return len(set(attrs_fields) - set(non_multi_fields)) == 0
    return True


@validate('form')
def valid_page_in_book(arch, **kwargs):
    """A `page` node must be below a `notebook` node."""
    return not arch.xpath('//page[not(ancestor::notebook)]')


@validate('graph')
def valid_field_in_graph(arch, **kwargs):
    """ Children of ``graph`` can only be ``field`` """
    return all(
        child.tag == 'field'
        for child in arch.xpath('/graph/*')
    )


@validate('tree')
def valid_field_in_tree(arch, **kwargs):
    """ Children of ``tree`` view must be ``field`` or ``button`` or ``control`` or ``groupby``."""
    return all(
        child.tag in ('field', 'button', 'control', 'groupby')
        for child in arch.xpath('/tree/*')
    )


@validate('form', 'graph', 'tree', 'activity')
def valid_att_in_field(arch, **kwargs):
    """ ``field`` nodes must all have a ``@name`` """
    return not arch.xpath('//field[not(@name)]')


@validate('form')
def valid_att_in_label(arch, **kwargs):
    """ ``label`` nodes must have a ``@for`` """
    return not arch.xpath('//label[not(@for) and not(descendant::input)]')


@validate('form')
def valid_att_in_form(arch, **kwargs):
    return True


@validate('form')
def valid_type_in_colspan(arch, **kwargs):
    """A `colspan` attribute must be an `integer` type."""
    return all(
        attrib.isdigit()
        for attrib in arch.xpath('//@colspan')
    )


@validate('form')
def valid_type_in_col(arch, **kwargs):
    """A `col` attribute must be an `integer` type."""
    return all(
        attrib.isdigit()
        for attrib in arch.xpath('//@col')
    )


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_alternative_image_text(arch, **kwargs):
    """An `img` tag must have an alt value."""
    if arch.xpath('//img[not(@alt or @t-att-alt or @t-attf-alt)]'):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_simili_button(arch, **kwargs):
    """A simili button must be tagged with "role='button'"."""
    # Select elements with class 'btn'
    xpath = '//a[contains(concat(" ", @class), " btn")'
    xpath += ' or contains(concat(" ", @t-att-class), " btn")'
    xpath += ' or contains(concat(" ", @t-attf-class), " btn")]'
    xpath += '[not(@role="button")]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_simili_dropdown(arch, **kwargs):
    """A simili dropdown must be tagged with "role='menu'"."""
    xpath = '//*[contains(concat(" ", @class, " "), " dropdown-menu ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " dropdown-menu ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " dropdown-menu ")]'
    xpath += '[not(@role="menu")]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_simili_progressbar(arch, **kwargs):
    """A simili progressbar must be tagged with "role='progressbar'" and have
    aria-valuenow, aria-valuemin and aria-valuemax attributes."""
    # Select elements with class 'btn'
    xpath = '//*[contains(concat(" ", @class, " "), " o_progressbar ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " o_progressbar ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " o_progressbar ")]'
    xpath += '[not(self::progress)]'
    xpath += '[not(@role="progressbar")]'
    xpath += '[not(@aria-valuenow or @t-att-aria-valuenow or @t-attf-aria-valuenow)]'
    xpath += '[not(@aria-valuemin or @t-att-aria-valuemin or @t-attf-aria-valuemin)]'
    xpath += '[not(@aria-valuemax or @t-att-aria-valuemax or @t-attf-aria-valuemax)]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_dialog(arch, **kwargs):
    """A dialog must use role="dialog" and its header, body and footer contents must use <header/>, <main/> and <footer/>."""
    # Select elements with class 'btn'
    xpath = '//*[contains(concat(" ", @class, " "), " modal ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " modal ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " modal ")]'
    xpath += '[not(@role="dialog")]'
    if arch.xpath(xpath):
        return "Warning"

    xpath = '//*[contains(concat(" ", @class, " "), " modal-header ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " modal-header ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " modal-header ")]'
    xpath += '[not(self::header)]'
    if arch.xpath(xpath):
        return "Warning"

    xpath = '//*[contains(concat(" ", @class, " "), " modal-body ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " modal-body ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " modal-body ")]'
    xpath += '[not(self::main)]'
    if arch.xpath(xpath):
        return "Warning"

    xpath = '//*[contains(concat(" ", @class, " "), " modal-footer ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " modal-footer ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " modal-footer ")]'
    xpath += '[not(self::footer)]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_simili_tabpanel(arch, **kwargs):
    """A tab panel with tab-pane class must have role="tabpanel"."""
    # Select elements with class 'btn'
    xpath = '//*[contains(concat(" ", @class, " "), " tab-pane ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " tab-pane ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " tab-pane ")]'
    xpath += '[not(@role="tabpanel")]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_simili_tab(arch, **kwargs):
    """A tab link must have role="tab", a link to an id (without #) by aria-controls."""
    # Select elements with class 'btn'
    xpath = '//*[@data-toggle="tab"]'
    xpath += '[not(@role="tab")'
    xpath += 'or not(@aria-controls or @t-att-aria-controls or @t-attf-aria-controls)'
    xpath += 'or contains(@aria-controls, "#") or contains(@t-att-aria-controls, "#")]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_simili_tablist(arch, **kwargs):
    """A tab list with class nav-tabs must have role="tablist"."""
    # Select elements with class 'btn'
    xpath = '//*[contains(concat(" ", @class, " "), " nav-tabs ")'
    xpath += ' or contains(concat(" ", @t-att-class, " "), " nav-tabs ")'
    xpath += ' or contains(concat(" ", @t-attf-class, " "), " nav-tabs ")]'
    xpath += '[not(@role="tablist")]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_focusable_button(arch, **kwargs):
    """A simili button must be with a `button`, an `input` (with type `button`, `submit` or `reset`) or a `a` tag."""
    xpath = '//*[contains(concat(" ", @class), " btn")'
    xpath += ' or contains(concat(" ", @t-att-class), " btn")'
    xpath += ' or contains(concat(" ", @t-attf-class), " btn")]'
    xpath += '[not(self::a)]'
    xpath += '[not(self::button)]'
    xpath += '[not(self::select)]'
    xpath += '[not(self::input[@type="button"])]'
    xpath += '[not(self::input[@type="submit"])]'
    xpath += '[not(self::input[@type="reset"])]'
    xpath += '[not(contains(@class, "btn-group"))]'
    xpath += '[not(contains(@t-att-class, "btn-group"))]'
    xpath += '[not(contains(@t-attf-class, "btn-group"))]'
    xpath += '[not(contains(@class, "btn-toolbar"))]'
    xpath += '[not(contains(@t-att-class, "btn-toolbar"))]'
    xpath += '[not(contains(@t-attf-class, "btn-toolbar"))]'
    xpath += '[not(contains(@class, "btn-ship"))]'
    xpath += '[not(contains(@t-att-class, "btn-ship"))]'
    xpath += '[not(contains(@t-attf-class, "btn-ship"))]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_prohibited_none_role(arch, **kwargs):
    """A role can't be `none` or `presentation`. All your elements must be accessible with screen readers, describe it."""
    xpath = '//*[@role="none" or @role="presentation"]'
    if arch.xpath(xpath):
        return "Warning"
    return True


@validate('calendar', 'diagram', 'form', 'graph', 'kanban', 'pivot', 'search', 'tree', 'activity')
def valid_alerts(arch, **kwargs):
    """An alert (class alert-*) must have an alert, alertdialog or status role. Please use alert and alertdialog only for what expects to stop any activity to be read immediatly."""
    xpath = '//*[contains(concat(" ", @class), " alert-")'
    xpath += ' or contains(concat(" ", @t-att-class), " alert-")'
    xpath += ' or contains(concat(" ", @t-attf-class), " alert-")]'
    xpath += '[not(contains(@class, "alert-link") or contains(@t-att-class, "alert-link")'
    xpath += ' or contains(@t-attf-class, "alert-link"))]'
    xpath += '[not(@role="alert")]'
    xpath += '[not(@role="alertdialog")]'
    xpath += '[not(@role="status")]'
    if arch.xpath(xpath):
        return "Warning"
    return True
=======
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
