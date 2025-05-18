import asyncio
import flet as ft
from utilities.debouncer import *
from utilities.fileUtils import *
from utilities.openApp import *
from utilities.listSorter import *
from utilities.searchUtils import *
from components.resultSection import *
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import dotenv_values
import os
from components.aiResponseContainer import *
from agentTools.agentTools import *
import multiprocessing
import time
from screeninfo import get_monitors
import pyautogui
from pynput import keyboard
import sys
from utilities.checkPermissions import *
from agents.mainAgent import MainAgent
from utilities.getResourcePath import get_asset_path
from rx.subject.behaviorsubject import BehaviorSubject
from states import thinkingStates, focusStates, resultsState


def adjust_window_height(mainColumn: ft.Column, page: ft.Page):
    match len(mainColumn.controls):
        case 1:
            page.window.height = 70
            page.title = f"{100}"
        case 2:
            if contains_element(mainColumn, "search_result_container"):
                page.window.height = 450
                page.title = f"{450}"

            if contains_element(mainColumn, "response"):
                page.window.height = 350
                page.title = f"{350}"

        case 3:
            page.window.height = 650
            page.title = f"{650}"


def remove_control_by_key(container: ft.Column, key: str):
    container.controls = [
        c for c in container.controls if getattr(c, "key", None) != key]


def contains_element(mainColumn: ft.Column, key: str):
    for c in mainColumn.controls:
        if getattr(c, "key") == key:
            return True
    return False


def debounced_search(query: str, latest_query: dict, page: ft.Page, mainColum: ft.Column):
    if not query.strip():
        remove_control_by_key(
            key="search_result_container", container=mainColum)
        adjust_window_height(mainColum, page)
        remove_control_by_key(
            key="response", container=mainColum)
        return
    if query != latest_query["value"]:
        return

    results = SearchUtils.search_files(query)
    sortedRes = ListSorter.sortListToDict(results)
    resultsState.previousResult = sortedRes

    if results:
        remove_control_by_key(
            key="search_result_container", container=mainColum)
        results_container = resultSection(sortedRes, page)
        result_main_container = ft.Container(
            key="search_result_container",
            height=370,
            content=results_container
        )
        mainColum.controls.append(result_main_container)
        adjust_window_height(mainColum, page)
        setState(page)
    else:
        remove_control_by_key(
            key="search_result_container", container=mainColum)
        adjust_window_height(mainColum, page)
        setState(page)


def expand_window(e: ft.ControlEvent, debouncer: Debouncer, page: ft.Page, mainColumn: ft.Column):
    query = e.control.value.strip()
    latest_query = {"value": ""}
    latest_query["value"] = query

    if not query:
        remove_control_by_key(
            key="search_result_container", container=mainColumn)
        remove_control_by_key(mainColumn, "response")
        adjust_window_height(mainColumn, page)
        setState(page)
        return
    else:
        if len(query) > 4:
            debouncer.callback = lambda: debounced_search(
                query, latest_query, page, mainColumn
            )
            debouncer.call()


async def searchBarEntered(e: str, mainColumn: ft.Column, page: ft.Page):
    remove_control_by_key(mainColumn, "response")
    mainColumn.controls.insert(1, AIResponseContainer(
        ft.Text("I am thinking...."), width=page.width, key="response", page=page))
    adjust_window_height(mainColumn, page)
    setState(page)
    res = await mainAgent.initiateMainAgent(e or "")

    remove_control_by_key(mainColumn, "response")
    mainColumn.controls.insert(1, AIResponseContainer(
        ft.Markdown(value=res, selectable=True,
                    shrink_wrap=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, code_theme=ft.MarkdownCodeTheme.DARCULA),
        width=page.width, key="response", res=res, page=page))  # type: ignore
    adjust_window_height(mainColumn, page)
    thinkingStates.Searching = False
    setState(page)


keys = dotenv_values(dotenv_path=get_asset_path(".env"))
mainAgent = MainAgent(apiKey=keys["GEMINI_API_KEY"]
                      or "", model="gemini-2.0-flash")


def onWindowEvent(event: ft.WindowEvent):
    if event.type == ft.WindowEventType.FOCUS:
        return
    if event.type == ft.WindowEventType.BLUR:
        return


def setState(page: ft.Page):
    page.update(page)


def handleKeyboardEvent(page: ft.Page, event: ft.KeyboardEvent, container: ft.Column):
    if (event.key == "Enter" and event.shift == True):
        if focusStates.currentIndex > 0:
            OpenApp.open(resultsState.resultPaths[focusStates.currentIndex-1])
    if (event.key == "Enter" and event.shift == False):
        print("hello")
        thinkingStates.Searching = True
        page.run_task(
            searchBarEntered, componentRef.searchBarRef.current.value or "", container, page)

    if (event.key == "Arrow Up"):
        if focusStates.currentIndex > 1:
            focusStates.currentIndex -= 1

            for ref in componentRef.resultContainersRef:
                for c in ref.current.controls:
                    if c.key == generateFocusKey(focusStates.currentIndex, "resultSection"):
                        c.bgcolor = "#263040"
                    elif c.key != None and "resultSection" in c.key:
                        c.bgcolor = "#1c2231"
            setState(page)
            if (scrollState.scrollReference != None):
                key = generateFocusKey(
                    focusStates.currentIndex, "resultSection")
                scrollState.scrollReference.current.scroll_to(
                    key=generateFocusKey(focusStates.currentIndex, "resultSection"), duration=200)
                if focusStates.currentIndex == 1:
                    scrollState.scrollReference.current.scroll_to(
                        offset=0, duration=200)
                setState(page)

    if (event.key == "Arrow Down"):
        if focusStates.itemIndex > focusStates.currentIndex:

            focusStates.currentIndex += 1
            if focusStates.currentIndex == 1:
                scrollState.scrollReference.current.scroll_to(
                    offset=0, duration=200)
            for ref in componentRef.resultContainersRef:
                for c in ref.current.controls:
                    if c.key == generateFocusKey(focusStates.currentIndex, "resultSection"):
                        c.bgcolor = "#263040"

                    elif c.key != None and "resultSection" in c.key:
                        c.bgcolor = "#1c2231"
            setState(page)
            if (scrollState.scrollReference != None):
                key = generateFocusKey(
                    focusStates.currentIndex, "resultSection")
                scrollState.scrollReference.current.scroll_to(
                    key=generateFocusKey(focusStates.currentIndex, "resultSection"), duration=200)
                setState(page)


async def main(page: ft.Page):
    page.window.on_event = onWindowEvent
    page.window.width = 620
    page.window.max_width = 620
    page.window.min_width = 620
    page.window.min_height = 70
    page.window.height = 100
    page.window.resizable = True
    page.window.frameless = True
    page.window.always_on_top = True
    page.title = f"{100}"
    page.bgcolor = "#1a1f2c"
    debouncer = Debouncer(0, None)
    mainColumn = ft.Column()
    search_bar_ref = Ref[ft.TextField]()

    page.on_keyboard_event = lambda event: handleKeyboardEvent(
        page, event, mainColumn)

    search = ft.TextField(
        hint_text="Search something...",
        ref=search_bar_ref,
        border_color="#403e43",
        bgcolor="#1d1f2a",
        on_change=lambda e: expand_window(e, debouncer, page, mainColumn),
        border_radius=12,
        hint_style=ft.TextStyle(color="#9b87f5"),
        suffix_icon=ft.Icon(ft.Icons.SEARCH, size=30, color="#9b87f5"),

    )
    componentRef.searchBarRef = search_bar_ref
    mainColumn.controls.append(search)

    page.add(mainColumn)

    CheckPermission.checkDiskPermission()


ft.app(target=main, view=None, port=8550)
# ft.app(target=main)
